# Odoo Web Addons

This repository contains Odoo addons related to the web interface.

## Building the javascript assets

Odoo's web interface is written in old javascript (ES2015). This allows to support older versions of web browsers.

Some module in this addon repository have assets written in ES6. The objective is to make these assets more
readable and easier to maintain.

[Webpack](https://webpack.js.org/) and Babel(https://babeljs.io/) are used to transpile these assets
into ES2015 compatible with older browsers.

To build the assets (for example with the module web_contextual_search_favorite):

```bash
npm install
cd web_contextual_search_favorite/static/src/js
webpack
```

## Testing

This repository includes Javascript tests written in ES6 with [AVA](https://github.com/avajs/ava).

To run the tests for the whole repository, simply run the following commands:

```bash
npm install
npm test
```
