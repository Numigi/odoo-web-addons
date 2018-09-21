/**
 * Extract the content from a domain filter.
 *
 * The given domain can either be an array or a raw string domain.
 *
 * For example, "[('partner_id', '=', 1), ('number', '=',' '123')]"
 * will return "('partner_id', '=', 1), ('number', '=',' '123')".
 *
 * @param {String | Array} the domain to parse
 * @returns {String} the content of the domain
 */

var _and = "\"&\"";
var _or = "\"|\"";
var _not = "\"!\"";

/**
 * Convert an array domain into a string domain.
 *
 * @param {Array} domain - the domain to convert into string
 * @returns {String} the converted domain
 */
function convertDomainArrayToString(domain){
    var domainIsMissingOuterParenthesis = (
        domain[0] &&
        domain[0] !== "&" && domain[0] !== "|" && domain[0] !== "!" &&
        !(domain[0] instanceof Array)
    );
    if(domainIsMissingOuterParenthesis){
        domain = [domain];
    }
    return JSON.stringify(domain);
}

/**
 * Extract the content of a domain filter.
 *
 * The regular expression extracts anything between the first opening and
 * the last closing parenthesis.
 *
 * It accepts spaces and chariot returns around the opening and closing parenthesis.
 *
 * @param {String | Array} domain - the domain for which to extract the content.
 * @returns {String} the domain content
 */
function extractContentFromDomain(domain){
    if(domain instanceof Array){
        domain = convertDomainArrayToString(domain);
    }

    var regex = /^\s*\[([\S\s]*)?\]\s*$/;
    var match = regex.exec(domain);
    if(match === null){
        throw new Error("Invalid domain filter " + domain);
    }
    return match[1] || "";
}

/**
 * Class responsible for splitting a domain content into an array of domain node strings.
 */
class DomainContentSplitter {

    /**
     * Seperate a domain content string into a list of domain node strings.
     *
     * @param {String} the domain content to split
     * @returns {Array} an array containing domain nodes
     */
    split(domainContent){
        this._domainNodes = [];
        this._currentNode = "";
        this._parenthesisCount = 0;

        domainContent.split("").forEach(char => this._processChar(char));

        this._domainNodes.push(this._currentNode);
        return this._domainNodes;
    }

    _processChar(char){
        if(this._isOpeningParenthesis(char)){
            this._processOpeningParenthesis(char);
        }
        else if(this._isClosingParenthesis(char)){
            this._processClosingParenthesis(char);
        }
        else if(this._isDomainNodeSeperator(char)){
            this._processDomainNodeSeperator(char);
        }
        else{
            this._currentNode += char;
        }
    }

    _processOpeningParenthesis(char){
        if(this._parenthesisCount === 0){
            this._domainNodes.push(this._currentNode);
            this._currentNode = "";
        }
        this._currentNode += char;
        this._parenthesisCount += 1;
    }

    _processClosingParenthesis(char){
        this._parenthesisCount -= 1;
        this._currentNode += char;
        if(this._parenthesisCount === 0){
            this._domainNodes.push(this._currentNode);
            this._currentNode = "";
        }
    }

    _processDomainNodeSeperator(char){
        this._domainNodes.push(this._currentNode);
        this._currentNode = "";
    }

    _isOpeningParenthesis(char){
        return char === "(" || char === "[";
    }

    _isClosingParenthesis(char){
        return char === ")" || char === "]";
    }

    _isDomainNodeSeperator(char){
        return this._parenthesisCount === 0 && char === ",";
    }
}


/**
 * Seperate a domain content string into a list of domain node strings.
 *
 * @param {String} the domain content to split
 * @returns {Array} an array containing domain nodes
 */
function _splitDomainNodes(domainContent){
    var domainNodes = new DomainContentSplitter().split(domainContent);

    // Exclude empty strings and strings containing only spaces
    return domainNodes.map(n => n.trim()).filter(n => n);
}


/**
 * Standardize quotes around & and | operators
 *
 * @param {String} domainContent - a domain content
 * @returns {String} the domain content with normalized operators.
 */
function _normalizeOperators(domainContent){
    return domainContent.replace("'&'", _and).replace("'|'", _or).replace("'!'", _not);
}


/**
 * Add explicit & operators to a domain content.
 *
 * In Odoo, & operators are implicit in a domain content when neither & not |
 * is specified. This methods adds explicit & operators where these are implicit.
 *
 * @param {String} the domain content with missing & operators
 * @returns {String} the content of the domain
 */
function addExplicitAndOperatorsToDomainContent(domainContent){
    domainContent = _normalizeOperators(domainContent);
    var domainNodes = _splitDomainNodes(domainContent);

    var operators = domainNodes.filter(n => n === _and || n === _or);
    var domainTuples = domainNodes.filter(n => n !== _and && n !== _or && n !== _not);

    // The total number of & and | operators must be equal to the number of domain tuples - 1.
    var missingAnds = _.times(domainTuples.length - operators.length - 1, _.constant(_and));
    return missingAnds.concat(domainNodes).join(", ");
}


/**
 * Merge the given domains using `&` operators into a single domain.
 *
 * @param {Array} the domains to merge
 * @returns {String} the resulting domain
 */
function mergeDomainsWithAndOperators(domains){
    var domainContents = domains.map(extractContentFromDomain).map(_normalizeOperators);
    return "[" + domainContents.join(", ") + "]";
}


/**
 * Merge the given domains using `|` operators into a single domain.
 *
 * @param {Array} the domains to merge
 * @returns {String} the resulting domain
 */
function mergeDomainsWithOrOperators(domains){
    var domainContents = domains.map(extractContentFromDomain);
    var domainContentsWithExplicitAnds = domainContents.map(addExplicitAndOperatorsToDomainContent);
    var ors = _.times(domainContentsWithExplicitAnds.length - 1, _.constant(_or));
    return "[" + ors.concat(domainContentsWithExplicitAnds).join(", ") + "]";
}


module.exports = {
    convertDomainArrayToString,
    extractContentFromDomain,
    addExplicitAndOperatorsToDomainContent,
    mergeDomainsWithAndOperators,
    mergeDomainsWithOrOperators,
};
