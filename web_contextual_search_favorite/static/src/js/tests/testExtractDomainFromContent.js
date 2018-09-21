
import test from "ava";
import {extractContentFromDomain, convertDomainArrayToString} from "../domainParsing";


test("Extract Content From Domain With Empty Domain", t => {
    var result = extractContentFromDomain("[]");
    t.true(result === "");
});

test("Extract Content From Domain With Single Domain", t => {
    var result = extractContentFromDomain("[('partner_id', '=', 1)]");
    t.true(result === "('partner_id', '=', 1)");
});

test("Extract Content From Domain With Spaces Around Domain", t => {
    var result = extractContentFromDomain(" [('partner_id', '=', 1)] ");
    t.true(result === "('partner_id', '=', 1)");
});

test("Extract Content From Domain With Multiple Line Domain", t => {
    var result = extractContentFromDomain("\n [\n ('partner_id', '=', 1) \n] \n");
    t.true(result === "\n ('partner_id', '=', 1) \n");
});

test("Extract Content From Domain With Multiple Node Domain", t => {
    var result = extractContentFromDomain("[('partner_id', '=', 1), ('number', '=', '123')]");
    t.true(result === "('partner_id', '=', 1), ('number', '=', '123')");
});

test("Extract Content From Domain With Or Operator", t => {
    var result = extractContentFromDomain("['|', ('partner_id', '=', 1), ('number', '=', '123')]");
    t.true(result === "'|', ('partner_id', '=', 1), ('number', '=', '123')");
});

test("Extract Content From Domain With And Operator", t => {
    var result = extractContentFromDomain("['&', ('partner_id', '=', 1), ('number', '=', '123')]");
    t.true(result === "'&', ('partner_id', '=', 1), ('number', '=', '123')");
});

test("Extract Content From Domain With Object Domain Containing And Operator", t => {
    var result = extractContentFromDomain(["&", ["partner_id", "=", 1], ["number", "=", "123"]]);
    t.true(result === "\"&\",[\"partner_id\",\"=\",1],[\"number\",\"=\",\"123\"]");
});

test("Extract Content From Domain With Object Domain Containing Or Operator", t => {
    var result = extractContentFromDomain(["|", ["partner_id", "=", 1], ["number", "=", "123"]]);
    t.true(result === "\"|\",[\"partner_id\",\"=\",1],[\"number\",\"=\",\"123\"]");
});

test("Extract Content From Domain With Object Domain Containing Not Operator", t => {
    var result = extractContentFromDomain(["!", ["partner_id", "=", 1], ["number", "=", "123"]]);
    t.true(result === "\"!\",[\"partner_id\",\"=\",1],[\"number\",\"=\",\"123\"]");
});
