/* © Numigi (tm) and all its contributors (https://numigi.com/r/home) */
/* License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('web_visual_company_switcher.CompanySwitcherWidget', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');
var rpc = require('web.rpc');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

var VisualCompanySwitcher = Widget.extend({
    template: 'VisualCompanySwitcher',
    
    events: {
        'click .visual-company-switcher-icon': '_openModal',
    },

    init: function () {
        this._super.apply(this, arguments);
        this.companies_data = null;
        this.current_allowed_companies = [];
        this._cacheTime = 0;
        this.selected_companies = [];
        this.multi_select_mode = false;
    },

    _openModal: function () {
        var self = this;
        
        // Load companies data and show modal directly
        this._loadCompaniesData().then(function () {
            self._showModal();
        }).catch(function () {
            // Error handling is already in _loadCompaniesData
        });
    },

    _loadCompaniesData: function () {
        var self = this;
        
        // Check cache (5 minutes TTL)
        var now = Date.now();
        if (this.companies_data && this._cacheTime && (now - this._cacheTime) < 300000) {
            return Promise.resolve(this.companies_data);
        }
        
        return rpc.query({
            route: '/web/visual_company_switcher/companies',
        }).then(function (result) {
            if (result.error) {
                self.displayNotification({
                    type: 'danger',
                    title: _t('Erreur'),
                    message: result.error,
                });
                return Promise.reject(result.error);
            }
            // Cache the data
            self.companies_data = result.companies || [];
            self.current_allowed_companies = result.current_allowed_companies || [];
            self._cacheTime = now;
            
            return self.companies_data;
        }).catch(function (error) {
            self.displayNotification({
                type: 'danger',
                title: _t('Erreur'),
                message: _t('Impossible de charger les données des compagnies.'),
            });
            return Promise.reject(error);
        });
    },

    _showModal: function () {
        var self = this;
        
        // Remove any existing modal first
        $('#visualCompanySwitcherModal').remove();
        
        var $modal = $(QWeb.render('visual_company_switcher_modal', {}));
        $modal.appendTo($('body'));
        
        $modal.modal('show');
        
        // Initialize orgchart after modal is shown
        $modal.on('shown.bs.modal', function () {
            self._initializeOrgChart($modal);
        });
        
        // Clean up when modal is closed
        $modal.on('hidden.bs.modal', function () {
            $modal.remove();
        });
        
        // Bind events - toggle switch
        $modal.find('#multiSelectToggle').on('change', function () {
            self.multi_select_mode = $(this).prop('checked');
            self._toggleMultiSelectMode($modal);
        });
        
        $modal.find('#applySelection').on('click', function () {
            self._applyMultipleSelection($modal);
        });
        
        $modal.find('#clearSelection').on('click', function () {
            self._clearAllSelections($modal);
        });
    },

    _initializeOrgChart: function ($modal) {
        var self = this;
        var $container = $modal.find('#orgchart-container');
        
        // Show loading spinner
        $container.html('<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" role="status"><span class="sr-only">Chargement...</span></div></div>');
        
        // Transform data for orgchart
        var orgData = this._transformDataForOrgChart();
        console.log('Transformed orgData:', JSON.stringify(orgData, null, 2));
        
        if (orgData.length === 0) {
            $container.html('<div class="alert alert-info">Aucune compagnie disponible</div>');
            return;
        }
        
        // Clear container and initialize orgchart
        $container.empty();
        var $orgChart = $('<div id="orgchart"></div>').appendTo($container);
        
        $orgChart.orgchart({
            'data': orgData[0], // Root company
            'nodeTemplate': function (data) {
                return self._renderCompanyNode(data);
            },
            'direction': 't2b', // Top to bottom
            'pan': true,
            'zoom': true,
            'toggleSiblingsResp': false, // Disable default sibling highlighting
            'createNode': function($node, data) {
                // Mark currently allowed companies with visual indicator
                if (self.current_allowed_companies.indexOf(data.id) !== -1) {
                    $node.addClass('currently-allowed');
                }
                
                // Add click handler when node is created
                $node.on('click.companyswitch', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    console.log('Node clicked!', data.id, 'Multi-select mode:', self.multi_select_mode);
                    console.log('Node classes before:', $node.attr('class'));
                    
                    if (self.multi_select_mode) {
                        // Multi-select mode - toggle selection with visual feedback
                        var isSelected = $node.find('.company-node').hasClass('multi-selected');
                        console.log('Is currently selected:', isSelected);
                        
                        if (isSelected) {
                            // Deselect
                            $node.find('.company-node').removeClass('multi-selected');
                            $node.find('.selection-badge').hide();
                            self.selected_companies = self.selected_companies.filter(id => id !== data.id);
                            console.log('Deselected company:', data.id);
                        } else {
                            // Select
                            $node.find('.company-node').addClass('multi-selected');
                            $node.find('.selection-badge').show();
                            if (self.selected_companies.indexOf(data.id) === -1) {
                                self.selected_companies.push(data.id);
                            }
                            console.log('Selected company:', data.id);
                        }
                        
                        console.log('Node classes after:', $node.attr('class'));
                        console.log('Node HTML:', $node[0].outerHTML);
                        console.log('Company node HTML:', $node.find('.company-node')[0] ? $node.find('.company-node')[0].outerHTML : 'NOT FOUND');
                        console.log('Selected companies:', self.selected_companies);
                        self._updateSelectionUI($modal);
                    } else {
                        // Single select mode - clear other selections and highlight current
                        console.log('Single select mode - clearing other selections');
                        $modal.find('.company-node').removeClass('single-selected');
                        // Find the company node and highlight it
                        var $companyNode = $modal.find('.company-node[data-company-id="' + data.id + '"]');
                        $companyNode.addClass('single-selected');
                        console.log('Company node classes after single select:', $companyNode.attr('class'));
                        self._switchToSingleCompany(data.id);
                    }
                });
                
                return $node;
            }
        });
        
        // No need for additional event binding - handled in createNode callback
    },

    _transformDataForOrgChart: function () {
        var companies = this.companies_data;
        var rootCompanies = companies.filter(function (company) {
            return !company.parent_id;
        });
        
        var self = this;
        function buildHierarchy(company) {
            var children = companies.filter(function (c) {
                return c.parent_id === company.id;
            });
            
            var node = {
                id: company.id,
                name: company.name,
                title: company.title,
                logo: company.logo,
                current: company.current,
                allowed: company.allowed,
            };
            
            if (children.length > 0) {
                node.children = children.map(buildHierarchy);
            }
            
            return node;
        }
        
        return rootCompanies.map(buildHierarchy);
    },

    _renderCompanyNode: function (data) {
        console.log('_renderCompanyNode called with data:', data);
        
        // Using structure inspired by OCA hr_org_chart_overview
        var nodeHtml = '<div class="company-node" data-company-id="' + data.id + '">';
        
        // Selection badge (hidden by default)
        nodeHtml += '<div class="selection-badge" style="display: none;">';
        nodeHtml += '<i class="fa fa-check-circle"></i>';
        nodeHtml += '</div>';
        
        // Current company badge (star icon)
        if (data.current) {
            nodeHtml += '<div class="current-badge">';
            nodeHtml += '<i class="fa fa-star"></i>';
            nodeHtml += '</div>';
        }
        
        // Logo section (like OCA's image span)
        nodeHtml += '<span class="company-image">';
        if (data.logo) {
            nodeHtml += '<img src="data:image/png;base64,' + data.logo + '" alt="Logo ' + _.escape(data.name) + '"/>';
        } else {
            nodeHtml += '<div class="company-logo-placeholder"><i class="fa fa-building"></i></div>';
        }
        nodeHtml += '</span>';
        
        // Company info (like OCA's title/content structure)
        nodeHtml += '<div class="company-title">' + _.escape(data.name) + '</div>';
        if (data.title && data.title !== data.name) {
            nodeHtml += '<div class="company-content">' + _.escape(data.title) + '</div>';
        }
        
        // Status indicator removed - using visual icons only
        
        nodeHtml += '</div>';
        console.log('Generated nodeHtml:', nodeHtml);
        return nodeHtml;
    },


    _toggleMultiSelectMode: function ($modal) {
        var $toggle = $modal.find('#multiSelectToggle');
        var $selectionInfo = $modal.find('#selectionInfo');
        var $applyButton = $modal.find('#applySelection');
        var $clearButton = $modal.find('#clearSelection');
        
        // Update toggle state to match mode
        $toggle.prop('checked', this.multi_select_mode);
        
        if (this.multi_select_mode) {
            // Switch to multi-select mode
            $selectionInfo.show();
            $applyButton.show();
            $clearButton.show();
            
            // Clear any single selections
            $modal.find('.company-node').removeClass('single-selected');
            
            // Pre-select currently allowed companies
            this.selected_companies = [...this.current_allowed_companies];
            this._highlightCurrentSelection($modal);
            this._updateSelectionUI($modal);
            
        } else {
            // Switch to single mode
            $selectionInfo.hide();
            $applyButton.hide();
            $clearButton.hide();
            
            // Clear all multi-selections
            this._clearAllSelections($modal);
        }
    },

    _updateSelectionUI: function ($modal) {
        var count = this.selected_companies.length;
        $modal.find('#selectionCount').text(count);
        $modal.find('#applyCount').text(count);
        
        // Enable/disable apply button
        var $applyButton = $modal.find('#applySelection');
        if (count > 0) {
            $applyButton.removeClass('btn-outline-success').addClass('btn-success');
        } else {
            $applyButton.removeClass('btn-success').addClass('btn-outline-success');
        }
    },
    
    _highlightCurrentSelection: function ($modal) {
        var self = this;
        // Clear existing selections first
        $modal.find('.company-node').removeClass('multi-selected');
        $modal.find('.selection-badge').hide();
        
        // Highlight selected companies
        this.selected_companies.forEach(function(company_id) {
            var $companyNode = $modal.find('.company-node[data-company-id="' + company_id + '"]');
            if ($companyNode.length) {
                $companyNode.addClass('multi-selected');
                $companyNode.find('.selection-badge').show();
                console.log('Highlighted company node:', company_id, $companyNode[0]);
            } else {
                console.log('Company node not found for ID:', company_id);
            }
        });
    },
    
    _clearAllSelections: function ($modal) {
        this.selected_companies = [];
        $modal.find('.company-node').removeClass('multi-selected');
        $modal.find('.selection-badge').hide();
        this._updateSelectionUI($modal);
    },

    _switchToSingleCompany: function (company_id) {
        var self = this;
        
        // Find company name for confirmation
        var company = this.companies_data.find(c => c.id === company_id);
        var companyName = company ? company.name : 'Compagnie inconnue';
        
        // Show confirmation dialog
        this._showConfirmationDialog(
            'Changer de compagnie',
            `Voulez-vous basculer vers "${companyName}" ?`,
            'Confirmer',
            'btn-primary',
            function() {
                self._performSingleSwitch(company_id);
            }
        );
    },
    
    _performSingleSwitch: function(company_id) {
        var self = this;
        
        rpc.query({
            route: '/web/visual_company_switcher/switch_company',
            params: {
                company_id: company_id,
            },
        }).then(function (result) {
            if (result.error) {
                self.displayNotification({
                    type: 'danger',
                    title: _t('Erreur'),
                    message: result.error,
                });
            } else if (result.success && result.reload) {
                self._softReload();
            }
        }).catch(function (error) {
            console.error('Company switch error:', error);
            self.displayNotification({
                type: 'danger',
                title: _t('Erreur'),
                message: _t('Une erreur est survenue lors du changement de compagnie.'),
            });
        });
    },

    _applyMultipleSelection: function ($modal) {
        var self = this;
        
        if (this.selected_companies.length === 0) {
            this.displayNotification({
                type: 'warning',
                title: _t('Attention'),
                message: _t('Veuillez sélectionner au moins une compagnie.'),
            });
            return;
        }
        
        // Show confirmation with company names
        var selectedNames = this.selected_companies.map(id => {
            var company = this.companies_data.find(c => c.id === id);
            return company ? company.name : `ID: ${id}`;
        });
        
        var message;
        if (this.selected_companies.length === 1) {
            message = `Utiliser "${selectedNames[0]}" comme compagnie active ?`;
        } else {
            message = `Utiliser ${this.selected_companies.length} compagnies sélectionnées ?\n\n• ${selectedNames.join('\n• ')}\n\nLa première sera la compagnie principale.`;
        }
        
        this._showConfirmationDialog(
            'Appliquer sélection',
            message,
            'Appliquer',
            'btn-success',
            function() {
                self._performMultipleSwitch();
            }
        );
    },
    
    _performMultipleSwitch: function() {
        var self = this;
        
        rpc.query({
            route: '/web/visual_company_switcher/switch_companies',
            params: {
                company_ids: this.selected_companies,
            },
        }).then(function (result) {
            if (result.error) {
                self.displayNotification({
                    type: 'danger',
                    title: _t('Erreur'),
                    message: result.error,
                });
            } else if (result.success && result.reload) {
                self._softReload();
            }
        }).catch(function (error) {
            console.error('Multiple companies switch error:', error);
            self.displayNotification({
                type: 'danger',
                title: _t('Erreur'),
                message: _t('Une erreur est survenue lors du changement de compagnies.'),
            });
        });
    },

    _showConfirmationDialog: function(title, message, confirmText, confirmClass, onConfirm) {
        var $dialog = $(`
            <div class="modal fade" id="companyConfirmModal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-sm" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${_.escape(title)}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p style="white-space: pre-line;">${_.escape(message)}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">
                                <i class="fa fa-times mr-1"></i>Annuler
                            </button>
                            <button type="button" class="btn ${confirmClass}" id="confirmAction">
                                <i class="fa fa-check mr-1"></i>${_.escape(confirmText)}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `);
        
        $dialog.appendTo($('body'));
        $dialog.modal('show');
        
        // Handle confirm action
        $dialog.find('#confirmAction').on('click', function() {
            $dialog.modal('hide');
            onConfirm();
        });
        
        // Clean up when closed
        $dialog.on('hidden.bs.modal', function () {
            $dialog.remove();
        });
    },

    _softReload: function () {
        // Instead of full page reload, trigger necessary updates
        var self = this;
        
        // Close the modal
        $('#visualCompanySwitcherModal').modal('hide');
        
        // Show success notification
        this.displayNotification({
            type: 'success',
            title: _t('Succès'),
            message: _t('Compagnie changée avec succès.'),
        });
        
        // Trigger web client reload (fallback to page reload for now)
        window.location.reload();
        
        // Clear cached data to force refresh next time
        this.companies_data = null;
        this._cacheTime = 0;
    },
});

// Systray menu item
var SystrayCompanySwitcher = Widget.extend({
    template: 'SystrayCompanySwitcher',
    
    init: function (parent) {
        this._super(parent);
        this.currentCompany = null;
    },
    
    start: function () {
        var self = this;
        return this._super().then(function () {
            return self._loadCurrentCompany();
        });
    },
    
    events: {
        'click .o_visual_company_switcher': '_openSwitcher',
    },

    _loadCurrentCompany: function () {
        var self = this;
        return rpc.query({
            route: '/web/visual_company_switcher/companies',
        }).then(function (result) {
            if (result.companies) {
                self.currentCompany = result.companies.find(function (company) {
                    return company.current;
                });
                self.allowedCompanies = result.current_allowed_companies || [];
                self._updateDisplay();
            }
        }).catch(function (error) {
            console.error('Failed to load current company:', error);
        });
    },
    
    _updateDisplay: function () {
        if (this.currentCompany) {
            var displayText = this.currentCompany.name;
            if (this.allowedCompanies && this.allowedCompanies.length > 1) {
                displayText += ' (+' + (this.allowedCompanies.length - 1) + ')';
            }
            this.$('.current-company-indicator').text(displayText);
        }
    },

    _openSwitcher: function () {
        var switcher = new VisualCompanySwitcher(this);
        switcher._openModal();
    },
});

SystrayMenu.Items.push(SystrayCompanySwitcher);

return {
    VisualCompanySwitcher: VisualCompanySwitcher,
    SystrayCompanySwitcher: SystrayCompanySwitcher,
};

});