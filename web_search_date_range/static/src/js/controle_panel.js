class ControlPanel extends Component {
        constructor() {
            super(...arguments);

            this.additionalContent = getAdditionalContent(this.props);

            useSubEnv({
                action: this.props.action,
                searchModel: this.props.searchModel,
                view: this.props.view,
            });

            // Connect to the model
            // TODO: move this in enterprise whenever possible
            if (this.env.searchModel) {
                this.model = useModel('searchModel');
            }

            // Reference hooks
            this.contentRefs = {
                buttons: useRef('buttons'),
                pager: useRef('pager'),
                searchView: useRef('searchView'),
                searchViewButtons: useRef('searchViewButtons'),
            };

            this.fields = this._formatFields(this.props.fields);
        }

        mounted() {
            this._attachAdditionalContent();
        }

        patched() {
            this._attachAdditionalContent();
        }

        async willUpdateProps(nextProps) {
            // Note: action and searchModel are not likely to change during
            // the lifespan of a ControlPanel instance, so we only need to update
            // the view information.
            if ('view' in nextProps) {
                this.env.view = nextProps.view;
            }
            if ('fields' in nextProps) {
                this.fields = this._formatFields(nextProps.fields);
            }
            this.additionalContent = getAdditionalContent(nextProps);
        }

        //---------------------------------------------------------------------
        // Private
        //---------------------------------------------------------------------

        /**
         * Attach additional content extracted from the props 'cp_content' key, if any.
         * @private
         */
        _attachAdditionalContent() {
            for (const key in this.additionalContent) {
                if (this.additionalContent[key] && this.additionalContent[key].length) {
                    const target = this.contentRefs[key].el;
                    if (target) {
                        target.innerHTML = "";
                        target.append(...this.additionalContent[key]);
                    }
                }
            }
        }

        /**
         * Give `name` and `description` keys to the fields given to the control
         * panel.
         * @private
         * @param {Object} fields
         * @returns {Object}
         */
        _formatFields(fields) {
            const formattedFields = {};
            for (const fieldName in fields) {
                formattedFields[fieldName] = Object.assign({
                    description: fields[fieldName].string,
                    name: fieldName,
                }, fields[fieldName]);
            }
            return formattedFields;
        }
    }