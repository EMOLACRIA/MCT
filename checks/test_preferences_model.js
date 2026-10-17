const fs=require('fs'),assert=require('assert'),path=require('path'),vm=require('vm');
const source=fs.readFileSync(path.resolve(__dirname,'../payload/style/shell/logic/Preferences.js'),'utf8').replace(/^\.pragma library\s*/,'');
const context=vm.createContext({});vm.runInContext(source,context,{timeout:1000});
const defaults=()=>JSON.parse(JSON.stringify(context.defaults()));
assert.strictEqual(context.validate(defaults()),'');
for(const [key,value] of [['fontScale',true],['fontScale',1.21],['fontScale',NaN],['reduceMotion',1],['surfaceOpacity',0.5],['terminal','sh -c bad'],['fileManager','../../bad.desktop'],['fileManager','bad.desktop\n'],['osdPosition','left']]) {
 const values=defaults();values[key]=value;assert(context.validate(values),key);
}
for(const [key,rule] of Object.entries(context.schema.fields)) {
 const values=defaults();if(rule.type==='number')values[key]=rule.max;else if(rule.type==='boolean')values[key]=!rule.default;else if(rule.enum)values[key]=rule.enum[rule.enum.length-1];
 assert.strictEqual(context.validate(values),'',key);
}
const unknown=defaults();delete unknown.fontScale;unknown.other=1;assert(context.validate(unknown));
assert(context.validate(null));assert(context.validate([]));assert(context.validate({}));
console.log('PASS: shared preference schema validation, boundaries, invalid types and application IDs.');
