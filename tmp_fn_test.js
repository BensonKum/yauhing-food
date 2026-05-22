
try {
    new Function(require("fs").readFileSync("tmp_final_check.js","utf8"));
    console.log("Function() parse: PASSED");
} catch(e) {
    console.log("Function() parse: FAILED - " + e.message);
}
