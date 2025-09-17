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
        this.companies_data = [];
        this.selected_companies = [];
        this.multi_select_mode = false;
    },

    _openModal: function () {
        var self = this;
        
        // Load companies data
        this._loadCompaniesData().then(function () {
            self._showModal();
        });
    },

    _loadCompaniesData: function () {
        var self = this;
        return rpc.query({
            route: '/web/visual_company_switcher/companies',
        }).then(function (data) {
            self.companies_data = data;
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
        
        // Bind events
        $modal.find('#multiSelectMode').on('change', function () {
            self.multi_select_mode = $(this).prop('checked');
            self._toggleMultiSelectMode($modal);
        });
        
        $modal.find('#applySelection').on('click', function () {
            self._applyMultipleSelection($modal);
        });
    },

    _initializeOrgChart: function ($modal) {
        var self = this;
        var $container = $modal.find('#orgchart-container');
        
        // Transform data for orgchart
        var orgData = this._transformDataForOrgChart();
        
        if (orgData.length === 0) {
            $container.html('<div class="alert alert-info">Aucune compagnie disponible</div>');
            return;
        }
        
        // Initialize orgchart
        var $orgChart = $('<div id="orgchart"></div>').appendTo($container);
        
        $orgChart.orgchart({
            'data': orgData[0], // Root company
            'nodeContent': function (data) {
                return self._renderCompanyNode(data);
            },
            'direction': 'b2t', // Bottom to top
            'pan': true,
            'zoom': true,
        });
        
        // Bind click events on company nodes
        this._bindNodeEvents($modal);
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
        var nodeHtml = '<div class="company-node" data-company-id="' + data.id + '">';
        
        // Checkbox (hidden by default)
        nodeHtml += '<div class="company-checkbox" style="display: none;">';
        nodeHtml += '<input type="checkbox" class="company-select" data-company-id="' + data.id + '"/>';
        nodeHtml += '</div>';
        
        // Logo
        if (data.logo) {
            nodeHtml += '<div class="company-logo">';
            nodeHtml += '<img src="' + data.logo + '" alt="Logo" class="img-fluid"/>';
            nodeHtml += '</div>';
        }
        
        // Name
        nodeHtml += '<div class="company-name">' + _.escape(data.name) + '</div>';
        
        // Current company badge
        if (data.current) {
            nodeHtml += '<div class="company-status">';
            nodeHtml += '<span class="badge badge-success">Active</span>';
            nodeHtml += '</div>';
        }
        
        nodeHtml += '</div>';
        return nodeHtml;
    },

    _bindNodeEvents: function ($modal) {
        var self = this;
        
        // Single click for single selection
        $modal.find('.company-node').on('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            
            var company_id = parseInt($(this).data('company-id'));
            
            if (self.multi_select_mode) {
                // Toggle selection in multi-select mode
                var $checkbox = $(this).find('.company-select');
                $checkbox.prop('checked', !$checkbox.prop('checked'));
                self._updateSelectedCompanies($modal);
            } else {
                // Single selection mode - switch immediately
                self._switchToSingleCompany(company_id);
            }
        });
        
        // Checkbox change event
        $modal.find('.company-select').on('change', function () {
            self._updateSelectedCompanies($modal);
        });
    },

    _toggleMultiSelectMode: function ($modal) {
        var $checkboxes = $modal.find('.company-checkbox');
        var $applyButton = $modal.find('#applySelection');
        
        if (this.multi_select_mode) {
            $checkboxes.show();
            $applyButton.show();
        } else {
            $checkboxes.hide();
            $applyButton.hide();
            // Clear selections
            $modal.find('.company-select').prop('checked', false);
            this.selected_companies = [];
        }
    },

    _updateSelectedCompanies: function ($modal) {
        var self = this;
        this.selected_companies = [];
        
        $modal.find('.company-select:checked').each(function () {
            var company_id = parseInt($(this).data('company-id'));
            self.selected_companies.push(company_id);
        });
        
        // Update visual selection
        $modal.find('.company-node').removeClass('selected');
        this.selected_companies.forEach(function (company_id) {
            $modal.find('.company-node[data-company-id="' + company_id + '"]').addClass('selected');
        });
    },

    _switchToSingleCompany: function (company_id) {
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
            } else if (result.reload) {
                window.location.reload();
            }
        }).catch(function (error) {
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
            } else if (result.reload) {
                window.location.reload();
            }
        }).catch(function (error) {
            self.displayNotification({
                type: 'danger',
                title: _t('Erreur'),
                message: _t('Une erreur est survenue lors du changement de compagnies.'),
            });
        });
    },
});

// Systray menu item
var SystrayCompanySwitcher = Widget.extend({
    template: 'SystrayCompanySwitcher',
    
    events: {
        'click .o_visual_company_switcher': '_openSwitcher',
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