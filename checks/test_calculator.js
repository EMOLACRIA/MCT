const assert=require('assert'),fs=require('fs'),path=require('path'),vm=require('vm');
const file=path.resolve(__dirname,'../payload/style/shell/logic/Calculator.js');
const source=fs.readFileSync(file,'utf8').replace(/^\.pragma library\s*/, '');
const context=vm.createContext({eval:()=>{throw Error('eval forbidden');},Function:()=>{throw Error('Function forbidden');}});
vm.runInContext(source,context,{filename:file,timeout:1000});
const calculate=text=>vm.runInContext('calculate('+JSON.stringify(text)+')',context,{timeout:100});
const examples=[
 ['2+3*4','14'],['(2+3)*4','20'],['  = (12 + 3) * 4 / 2 ','30'],
 ['-.5 + 1.25','0.75'],['1,5+2.25','3.75'],['2--3','5'],['+3 * -2','-6'],
 ['2^3^2','512'],['-2^2','-4'],['(-2)^2','4'],['2^-2','0.25'],
 ['50%','0.5'],['200 * 10%','20'],['200 + 10%','200.1'],['(20+30)%','0.5'],
 ['2 × 3 − 4 ÷ 2','4'],['1e3 + 2E-2','1000.02'],['0.1+0.2','0.3'],
 ['1/3','0.333333333333'],['-0','0'],['1e100','1e+100']
];
for(const [input,text] of examples){const r=calculate(input);assert.strictEqual(r.state,'ready',input+': '+r.message);assert.strictEqual(r.text,text,input);assert(Number.isFinite(r.value));}
for(const input of ['', 'spotify','dolphin','3D','1password','2fa','code editor','echo 2+3','$(touch /tmp/x)'])assert.strictEqual(calculate(input).state,'none',input);
for(const input of ['=','2+','(2+3','1e-','-','.','2^','2/'])assert.strictEqual(calculate(input).state,'incomplete',input);
for(const input of ['1/0','0/0','1e999','10^999','(-2)^0.5','2(3)','1,000.25','2..3','2**3','2+)', '=alert(1)', '=process.exit()', '=1;2']) {
 const result=calculate(input);assert.strictEqual(result.state,'error',input+': '+JSON.stringify(result));assert.strictEqual(result.text,'');
}
for(const input of ['='.repeat(2)+'2','=a.constructor.constructor("return 1")()', '="<script>"'])assert.strictEqual(calculate(input).state,'error',input);
for(const input of ['('.repeat(40)+'1'+')'.repeat(40),'-'.repeat(40)+'1', '1+'.repeat(200)+'1','1'.repeat(513)])assert.strictEqual(calculate(input).state,'error');
// Every returned display value can be pasted back into this same grammar.
for(const [input] of examples)assert.strictEqual(calculate(calculate(input).text).state,'ready',input);
// Deterministic malformed input: bounded parser work and no escaping exceptions.
let seed=29;const alphabet='0123+-*/^%()e.,';
for(let i=0;i<300;i++){let s='=';for(let j=0;j<40;j++){seed=(seed*1664525+1013904223)>>>0;s+=alphabet[seed%alphabet.length];}const r=calculate(s);assert(['ready','incomplete','error'].includes(r.state));}
console.log('PASS: arithmetic, precedence, decimals, percentages, incomplete/error states, application queries, input bounds and 300 malformed expressions.');
