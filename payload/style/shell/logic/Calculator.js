.pragma library

// A small arithmetic grammar shared by every launcher presentation.
// Percent is a postfix division by 100, never a contextual discount or modulo.
function calculate(input) {
    var source=String(input === null || input === undefined ? "" : input).trim();
    var forced=source.charAt(0)==="=";
    if(forced)source=source.slice(1).trim();
    source=source.replace(/×/g,"*").replace(/÷/g,"/").replace(/−/g,"-");
    if(!forced && (!/^[0-9.(,+-]/.test(source) || !/^[0-9eE+\-*/^%().,\s]*$/.test(source)))return {state:"none",text:"",message:""};
    if(source.length>512)return {state:"error",text:"",message:"Expression is too long (512 characters max)"};
    var tokens=[],position=0,index=0,depth=0;
    function fail(state,message) {throw {state:state,text:"",message:message};}
    function finite(value) {
        if(!Number.isFinite(value))fail("error","Result is outside the supported range");
        return value;
    }
    try {
        while(position<source.length) {
            var rest=source.slice(position),c=rest.charAt(0);
            if(/\s/.test(c)) {position++;continue;}
            if(/[0-9.,]/.test(c)) {
                var number=rest.match(/^(?:\d+(?:[.,]\d*)?|[.,]\d+)/);
                if(!number) {
                    if(position===source.length-1)fail("incomplete","Continue the expression…");
                    fail("error","Use a decimal point or comma, without digit grouping");
                }
                var literal=number[0].replace(",",".");position+=number[0].length;
                if(/[eE]/.test(source.charAt(position)) && position<source.length) {
                    literal+=source.charAt(position++);
                    if(/[+-]/.test(source.charAt(position)) && position<source.length)literal+=source.charAt(position++);
                    var exponent=source.slice(position).match(/^\d+/);
                    if(!exponent)fail(position===source.length ? "incomplete" : "error","Complete the exponent");
                    literal+=exponent[0];position+=exponent[0].length;
                }
                tokens.push({kind:"number",value:finite(Number(literal))});
            } else if("+-*/^%()".indexOf(c)>=0) {tokens.push({kind:c});position++;}
            else fail("error","Use numbers, parentheses and arithmetic operators");
            if(tokens.length>256)fail("error","Expression has too many terms");
        }
        function kind() {return index<tokens.length ? tokens[index].kind : "end";}
        function nested(fn) {
            if(++depth>32)fail("error","Expression is nested too deeply");
            var value=fn();depth--;return value;
        }
        function primary() {
            if(kind()==="number")return tokens[index++].value;
            if(kind()==="(") {
                index++;var value=nested(sum);
                if(kind()!==")")fail(kind()==="end" ? "incomplete" : "error","Close the parenthesis");
                index++;return value;
            }
            fail(kind()==="end" ? "incomplete" : "error",kind()==="end" ? "Continue the expression…" : "Expected a number or parenthesis");
        }
        function postfix() {var value=primary();while(kind()==="%") {index++;value/=100;}return value;}
        function power() {var value=postfix();if(kind()==="^") {index++;value=finite(Math.pow(value,nested(unary)));}return value;}
        function unary() {
            if(kind()==="+" || kind()==="-") {var sign=tokens[index++].kind;var value=nested(unary);return sign==="-" ? -value : value;}
            return power();
        }
        function product() {
            var value=unary();
            while(kind()==="*" || kind()==="/") {
                var op=tokens[index++].kind,right=unary();
                if(op==="/" && right===0)fail("error","Cannot divide by zero");
                value=finite(op==="*" ? value*right : value/right);
            }
            return value;
        }
        function sum() {
            var value=product();
            while(kind()==="+" || kind()==="-") {var op=tokens[index++].kind,right=product();value=finite(op==="+" ? value+right : value-right);}
            return value;
        }
        var result=finite(sum());
        if(index!==tokens.length)fail("error","Check the operators and parentheses");
        // IEEE-754 arithmetic; 12 significant digits keep ordinary results legible.
        var text=String(Number(result.toPrecision(12)));
        return {state:"ready",text:text,message:"",value:result};
    } catch(error) {
        if(error && (error.state==="error" || error.state==="incomplete"))return error;
        return {state:"error",text:"",message:"Cannot calculate this expression"};
    }
}
