
import test from "ava";
import {mergeDomainsWithAndOperators, mergeDomainsWithOrOperators} from "../domainParsing";

var domain1 = "[('a', '=', 1)]";
var domain2 = "[('b', '=', 1), ('b', '=', 2)]";
var domain3 = "['|', ('c', '=', 3), ('d', '=', 4)]";

test("Merge 2 Domains Using And Operators", t => {
    var result = mergeDomainsWithAndOperators([domain1, domain2]);
    t.true(result === "[('a', '=', 1), ('b', '=', 1), ('b', '=', 2)]");
});

test("Merge 3 Domains Using And Operators", t => {
    var result = mergeDomainsWithAndOperators([domain1, domain2, domain3]);
    t.true(result === "[('a', '=', 1), ('b', '=', 1), ('b', '=', 2), \"|\", ('c', '=', 3), ('d', '=', 4)]");
});

test("Merge 2 Domains Using Or Operators", t => {
    var result = mergeDomainsWithOrOperators([domain1, domain2]);
    t.true(result === "[\"|\", ('a', '=', 1), \"&\", ('b', '=', 1), ('b', '=', 2)]");
});

test("Merge 3 Domains Using Or Operators", t => {
    var result = mergeDomainsWithOrOperators([domain1, domain2, domain3]);
    t.true(result === "[\"|\", \"|\", ('a', '=', 1), \"&\", ('b', '=', 1), ('b', '=', 2), \"|\", ('c', '=', 3), ('d', '=', 4)]");
});

test("Merge An Array Domain With Missing Outer Parenthesis", t => {
    var domainArray = ["a", "=", 1];
    var domainStr = `["&", ('b', '=', 1), ('b', '=', 2)]`;
    var result = mergeDomainsWithAndOperators([domainArray, domainStr]);
    t.true(result === "[[\"a\",\"=\",1], \"&\", ('b', '=', 1), ('b', '=', 2)]");
});

test("Merge An Array Domain Beginning With Operator", t => {
    var domainArray = ["&", ["a", "=", 1], ["a", "=", 2]];
    var domainStr = "['&', ('b', '=', 1), ('b', '=', 2)]";
    var result = mergeDomainsWithAndOperators([domainArray, domainStr]);
    t.true(result === "[\"&\",[\"a\",\"=\",1],[\"a\",\"=\",2], \"&\", ('b', '=', 1), ('b', '=', 2)]");
});

var emptyDomains = [
    [], "[]", "[ ]",
];

/**
 * When merging a domain with an empty domain using AND, the empty domain is ignored.
 */
test("Merge Domain With Empty Domain", t => {
    emptyDomains.forEach((emptyDomain) => {
        var result = mergeDomainsWithAndOperators([emptyDomain, domain1]);
        t.true(result === "[('a', '=', 1)]");
    });
});

test("Merge Domain With Empty Domain (empty domain after)", t => {
    emptyDomains.forEach((emptyDomain) => {
        var result = mergeDomainsWithAndOperators([domain1, emptyDomain]);
        t.true(result === "[('a', '=', 1)]");
    });
});

/**
 * When merging a domain with an empty domain using OR, the resulting domain is empty.
 */
test("Merge Domain With Empty Domain Using Or Operator", t => {
    emptyDomains.forEach((emptyDomain) => {
        var result = mergeDomainsWithOrOperators([emptyDomain, domain1]);
        t.true(result === "[]");
    });
});

test("Merge Domain With Empty Domain Using Or Operator (empty domain after)", t => {
    emptyDomains.forEach((emptyDomain) => {
        var result = mergeDomainsWithOrOperators([domain1, emptyDomain]);
        t.true(result === "[]");
    });
});
