odoo.define('resize_observer_error_catcher.handling_error', function (require) {
    "use strict";

window.addEventListener('error', (e) => {
if (
    [
    'ResizeObserver loop completed with undelivered notifications.',
    'ResizeObserver loop limit exceeded',
    /* add more if needed */
    ].includes(e.message)
) {
    e.stopImmediatePropagation();
}
});

});