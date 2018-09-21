
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
