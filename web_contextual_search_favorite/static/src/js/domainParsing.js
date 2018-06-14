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
function extractContentFromDomain(domain){
    if(domain instanceof Array){
        domain = JSON.stringify(domain);
    }
    var regex = /^\s*\[([\S\s]*)?\]\s*$/;
    var match = regex.exec(domain);
    if(match === null){
        throw new Error("Invalid domain filter " + domain);
    }
    return match[1] || "";
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
    var and = "\"&\"";
    var or = "\"|\"";
    var not = "\"!\"";

    // Standardize quotes around & and | operators
    domainContent = domainContent.replace("'&'", and).replace("'|'", or).replace("'!'", not);

    domainNodes = _splitDomainNodes(domainContent);

    var operators = domainNodes.filter(function(n){return n === and || n === or;});
    var domainTuples = domainNodes.filter(function(n){return n !== and && n !== or && n !== not;});

    // The total number of & and | operators must be equal to the number of domain tuples - 1.
    var missingAnds = _.times(domainTuples.length - operators.length - 1, _.constant(and));
    return missingAnds.concat(domainNodes).join(", ");
}

/**
 * Seperate a domain content string into a list of domain node strings.
 *
 * @param {String} the domain content to split
 * @returns {Array} an array containing domain nodes
 */
function _splitDomainNodes(domainContent){
    var domainNodes = [];
    var currentNode = "";
    var parenthesisCount = 0;

    // Iterate around each caracters
    //
    // When encountering an opening, a closing parenthesis or a comma,
    // we determine whether a domain part begins or ends.
    for(var i = 0; i < domainContent.length; i++){
        var char = domainContent[i];

        if(char === "(" || char === "["){
            if(parenthesisCount === 0){
                domainNodes.push(currentNode);
                currentNode = "";
            }
            currentNode += char;
            parenthesisCount += 1;
        }
        else if(char === ")" || char === "]"){
            parenthesisCount -= 1;
            currentNode += char;
            if(parenthesisCount === 0){
                domainNodes.push(currentNode);
                currentNode = "";
            }
        }
        else if(parenthesisCount === 0 && char === ","){
            domainNodes.push(currentNode);
            currentNode = "";
        }
        else{
            currentNode += char;
        }
    }

    domainNodes.push(currentNode);

    // Exclude empty strings and strings containing only spaces
    return domainNodes.map(function(n){return n.trim();}).filter(function(n){return n;});  
}

module.exports = {
    extractContentFromDomain,
    addExplicitAndOperatorsToDomainContent,
}
