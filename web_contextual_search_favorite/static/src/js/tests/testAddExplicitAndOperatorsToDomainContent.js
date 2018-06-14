
import test from "ava";
import {addExplicitAndOperatorsToDomainContent} from "../domainParsing";

var and = "\"&\", ";
var or = "\"|\", ";
var not = "\"!\", ";
var comma = ", ";

var domainTuple1 = "('partner_id', '=', 1)";
var domainTuple2 = "('number', '=', '123')";
var domainTuple3 = "('partner_id.code', '=', '456')";

test("Add And Operators With Empty Domain Content", t => {
    var result = addExplicitAndOperatorsToDomainContent("");
    t.true(result === "");
});

test("Add And Operators With Single Tuple Domain", t => {
    var domain = domainTuple1;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === domain);
});

test("Add And Operators With 2 Tuples Domain", t => {
    var domain = domainTuple1 + comma + domainTuple2;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === and + domain);
});

test("Add And Operators With 2 Tuples Domain And One Operator", t => {
    var domain = and + domainTuple1 + comma + domainTuple2;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === domain);
});

test("Add And Operators With 2 Tuples Domain And One Negative Operator", t => {
    var domain = not + domainTuple1 + comma + domainTuple2;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === and + domain);
});

test("Add And Operators With 3 Tuples Domain", t => {
    var domain = domainTuple1 + comma + domainTuple2 + comma + domainTuple3;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === and + and + domain);
});

test("Add And Operators With 3 Tuples Domain And One Operator", t => {
    var domain = or + domainTuple1 + comma + domainTuple2 + comma + domainTuple3;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === and + domain);
});

test("Add And Operators With 3 Tuples Domain And Tow Operators", t => {
    var domain = or + domainTuple1 + comma + and + domainTuple2 + comma + domainTuple3;
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === domain);
});

test("Add And Operators With Single Array Domain", t => {
    var domain = domainTuple1.replace("(", "[").replace(")", "]");
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === domain);
});

test("Add And Operators With 2 Array Domain And One Negative Operator", t => {
    var domain = (not + domainTuple1 + comma + domainTuple2).replace("(", "[").replace(")", "]");
    var result = addExplicitAndOperatorsToDomainContent(domain);
    t.true(result === and + domain);
});
