(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2e87cd74"],{"21c9":function(e,t,a){"use strict";var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-row",{style:e.mainStyle,attrs:{type:"flex",justify:"left"}},[a("el-col",[a("el-date-picker",{attrs:{type:"year",placeholder:"起始年份"},on:{change:e.beginChange},model:{value:e.beginYearInternal,callback:function(t){e.beginYearInternal=t},expression:"beginYearInternal"}})],1),a("el-col",{staticStyle:{margin:"auto","text-align":"center",color:"lightgray","font-size":"12px"}},[e._v(" 至 ")]),a("el-col",[a("el-date-picker",{attrs:{type:"year",placeholder:"终止年份"},on:{change:e.endChange},model:{value:e.endYearInternal,callback:function(t){e.endYearInternal=t},expression:"endYearInternal"}})],1)],1)},r=[],l={name:"YearRangeSelector",props:["beginYear","endYear","expand"],data:function(){return{beginYearInternal:this.beginYear,endYearInternal:this.endYear}},methods:{beginChange:function(e){null===e?this.$emit("update:beginYear",null):this.$emit("update:beginYear",e.getFullYear())},endChange:function(e){null===e?this.$emit("update:endYear",null):this.$emit("update:endYear",e.getFullYear())}},watch:{beginYearInternal:function(e){null!==e?this.$emit("update:beginYear",e.getFullYear()):this.$emit("update:beginYear",null)},endYearInternal:function(e){null!==e?this.$emit("update:endYear",e.getFullYear()):this.$emit("update:endYear",null)},beginYear:function(e){this.beginYearInternal=null!==e?new Date(e,1,1):null},endYear:function(e){this.endYearInternal=null!==e?new Date(e,1,1):null}},computed:{mainStyle:function(){return this.expand?"":"width: 55%"}}},i=l,s=(a("6e83"),a("2877")),o=Object(s["a"])(i,n,r,!1,null,"7bfa7c13",null);t["a"]=o.exports},"340d":function(e,t,a){"use strict";a.d(t,"a",(function(){return n}));a("d81d");function n(e){return e.map((function(e){return{key:e,label:e,value:e}}))}},"37d3":function(e,t,a){},"6e83":function(e,t,a){"use strict";a("e4af")},a93a:function(e,t,a){"use strict";var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-form",{attrs:{"label-position":"right","label-width":"auto"}},["industry"===e.placeOrIndustry?a("el-form-item",{attrs:{label:"预测行业："}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.postParams.industry,callback:function(t){e.$set(e.postParams,"industry",t)},expression:"postParams.industry"}},e._l(e.predictIndustries,(function(e){return a("el-option",{key:e,attrs:{value:e,label:e}})})),1)],1):e._e(),"place"===e.placeOrIndustry?a("el-form-item",{attrs:{label:"预测地区："}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.postParams.region,callback:function(t){e.$set(e.postParams,"region",t)},expression:"postParams.region"}},e._l(e.predictRegions,(function(e){return a("el-option",{key:e,attrs:{value:e,label:e}})})),1)],1):e._e(),a("el-form-item",{attrs:{label:"历史年份："}},[a("year-range-selector",{attrs:{"begin-year":e.postParams.historyBeginYear,"end-year":e.postParams.historyEndYear},on:{"update:beginYear":function(t){return e.$set(e.postParams,"historyBeginYear",t)},"update:begin-year":function(t){return e.$set(e.postParams,"historyBeginYear",t)},"update:endYear":function(t){return e.$set(e.postParams,"historyEndYear",t)},"update:end-year":function(t){return e.$set(e.postParams,"historyEndYear",t)}}})],1),a("el-form-item",{attrs:{label:"预测年份："}},[a("year-range-selector",{attrs:{"begin-year":e.postParams.beginYear,"end-year":e.postParams.endYear},on:{"update:beginYear":function(t){return e.$set(e.postParams,"beginYear",t)},"update:begin-year":function(t){return e.$set(e.postParams,"beginYear",t)},"update:endYear":function(t){return e.$set(e.postParams,"endYear",t)},"update:end-year":function(t){return e.$set(e.postParams,"endYear",t)}}})],1),a("el-form-item",{attrs:{label:"选择组合模型："}},[a("el-select",{attrs:{multiple:"",placeholder:"请选择"},model:{value:e.postParams.selectedMethods,callback:function(t){e.$set(e.postParams,"selectedMethods",t)},expression:"postParams.selectedMethods"}},e._l(e.allMethods,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),a("el-form-item",{attrs:{label:"方案标签："}},[a("el-input",{attrs:{clearable:"",placeholder:"可留空"},model:{value:e.postParams.tag,callback:function(t){e.$set(e.postParams,"tag",t)},expression:"postParams.tag"}})],1),a("el-form-item",{attrs:{label:"加载方案："}},[a("el-select",{staticStyle:{width:"50%"},attrs:{placeholder:"选择标签",size:"small"},model:{value:e.currentTag,callback:function(t){e.currentTag=t},expression:"currentTag"}},e._l(e.knownTags,(function(e){return a("el-option",{key:e.id,attrs:{label:e.id,value:e.id}})})),1),a("el-button",{staticStyle:{"margin-left":"10px"},attrs:{size:"small",disabled:null===e.currentTag},on:{click:e.loadParameters}},[e._v("加载")])],1),a("el-form-item",[a("el-button",{attrs:{disabled:0===e.postParams.selectedMethods.length},on:{click:e.validate}},[e._v("检测")]),a("el-button",{attrs:{type:"primary",disabled:!e.canCommitQuery},on:{click:e.performQuery}},[e._v("预测")])],1)],1)},r=[],l=a("340d"),i=a("21c9"),s={name:"MixPredictSelectForm",props:["placeOrIndustry","graphData","tableOneData","tableTwoData"],components:{YearRangeSelector:i["a"]},data:function(){return{postParams:{historyBeginYear:null,historyEndYear:null,beginYear:null,endYear:null,region:"",industry:"",selectedMethods:[],tag:null,tagType:"MIX"},graphDataInternal:[],tableOneDataInternal:[],tableTwoDataInternal:[],predictRegions:[],predictIndustries:[],originalAllMethodsForPlace:[],originalAllMethodsForIndustry:[],knownTags:[],currentTag:null}},mounted:function(){"place"===this.placeOrIndustry?(this.loadRegions(),this.loadRegionalMethods()):(this.loadIndustries(),this.loadIndustrialMethods()),this.loadTags()},methods:{loadParameters:function(){var e=this;this.$axios.get("/params/predict/mix",{params:{tag:this.$data.currentTag}}).then((function(t){e.$data.postParams=t.data.data}))},loadTags:function(){var e=this;this.$axios.get("/tags/query",{params:{tagType:"MIX"}}).then((function(t){e.$data.knownTags=t.data.data}))},loadRegions:function(){var e=this;this.$axios.get("/region/query").then((function(t){e.$data.predictRegions=t.data.data}))},loadIndustries:function(){var e=this;this.$axios.get("/industry/query").then((function(t){e.$data.predictIndustries=t.data.data}))},loadIndustrialMethods:function(){var e=this;this.$axios.get("/method/industry/query").then((function(t){e.$data.originalAllMethodsForIndustry=t.data.data}))},loadRegionalMethods:function(){var e=this;this.$axios.get("/method/region/query").then((function(t){e.$data.originalAllMethodsForPlace=t.data.data}))},validate:function(){var e=this;this.$axios.post(this.validateUrl,{methods:this.$data.postParams.selectedMethods}).then((function(t){var a=t.data.data.ok;a?e.$messenger.success("这组组合模型符合要求。"):e.$messenger.warning("这组组合模型不符合要求。")}))},performQuery:function(){var e=this;this.$axios.post(this.commitUrl,this.$data.postParams).then((function(t){e.$data.graphDataInternal=t.data.data.graphData,e.$data.tableOneDataInternal=t.data.data.tableOneData,e.$data.tableTwoDataInternal=t.data.data.tableTwoData}))}},computed:{allMethods:function(){return"place"===this.placeOrIndustry?Object(l["a"])(this.originalAllMethodsForPlace):Object(l["a"])(this.originalAllMethodsForIndustry)},commitUrl:function(){return"place"===this.placeOrIndustry?"/predict/region/mix":"/predict/industry/mix"},validateUrl:function(){return"".concat(this.commitUrl,"/validate")},canCommitQuery:function(){var e=this.$data.postParams;if(null===e.beginYear||null===e.endYear)return!1;if(null===e.historyBeginYear||null===e.historyEndYear)return!1;if("industry"===this.placeOrIndustry){if(0===e.industry.length)return!1}else if("place"===this.placeOrIndustry&&0===e.region.length)return!1;return 0!==e.selectedMethods.length}},watch:{graphDataInternal:function(e){this.$emit("update:graphData",e)},tableOneDataInternal:function(e){this.$emit("update:tableOneData",e)},tableTwoDataInternal:function(e){this.$emit("update:tableTwoData",e)}}},o=s,u=(a("c64a"),a("2877")),d=Object(u["a"])(o,n,r,!1,null,"2a53a2a0",null);t["a"]=d.exports},c3ab:function(e,t,a){"use strict";var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{directives:[{name:"show",rawName:"v-show",value:e.graphData.length>0,expression:"graphData.length > 0"}],staticStyle:{"margin-left":"20px"}},[a("el-row",[a("div",{staticStyle:{width:"680px",height:"300px"},attrs:{id:e.uniqueId}})]),a("el-row",[a("el-form",[a("el-form-item",[a("el-button",{on:{click:e.exportImage}},[e._v("导出图像")])],1),a("el-form-item",{attrs:{label:"显示方式："}},[a("el-select",{attrs:{placeholder:"请选择"},model:{value:e.currentDisplayMethod,callback:function(t){e.currentDisplayMethod=t},expression:"currentDisplayMethod"}},e._l(e.displayMethods,(function(e){return a("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1)],1)],1)],1)},r=[],l=(a("4160"),a("d3b7"),a("ac1f"),a("1276"),a("5cc6"),a("9a8c"),a("a975"),a("735e"),a("c1ac"),a("d139"),a("3a7b"),a("d5d6"),a("82f8"),a("e91f"),a("60bd"),a("5f96"),a("3280"),a("3fcc"),a("ca91"),a("25a1"),a("cd26"),a("3c5d"),a("2954"),a("649e"),a("219c"),a("170b"),a("b39a"),a("72f7"),a("159b"),a("313e")),i=a("21a6");function s(e){for(var t=e.split(";base64,"),a=t[0].split(":")[1],n=window.atob(t[1]),r=n.length,l=new Uint8Array(r),i=0;i<r;++i)l[i]=n.charCodeAt(i);return new Blob([l],{type:a})}var o={data:function(){return{currentChart:void 0,graphData:[],params1st:{xTag:"xName",yTag:"yValue",xName:"",yName:""},params2nd:{xTag:"",yTag1st:"",yTag2nd:"",xName:"",yName:"",yName1st:"",yName2nd:""},displayMethods:[{label:"折线图",value:"line"},{label:"柱状图",value:"bar"},{label:"散点图",value:"scatter"}],currentDisplayMethod:"line"}},methods:{refreshChart:function(){var e=this.$data.params1st;void 0===this.currentChart&&(this.currentChart=l["init"](document.getElementById(this.uniqueId)));var t=[],a=[];this.$data.graphData.forEach((function(n){t.push(n[e.xTag]),a.push(n[e.yTag])}));var n={xAxis:{type:"category",name:e.xName,data:t},yAxis:{type:"value",name:e.yName},series:[{data:a,name:e.yName,type:this.$data.currentDisplayMethod}],legend:{orient:"horizontal",x:"center",y:"top"}};this.currentChart.setOption(n,!0)},refreshChart2nd:function(){var e=this.$data.params2nd;void 0===this.currentChart&&(this.currentChart=l["init"](document.getElementById(this.uniqueId)));var t=[],a=[],n=[];this.$data.graphData.forEach((function(r){t.push(r[e.xTag]),a.push(r[e.yTag1st]),n.push(r[e.yTag2nd])}));var r={xAxis:{type:"category",name:e.xName,data:t},yAxis:{type:"value",name:e.yName},series:[{data:a,name:e.yName1st,type:this.$data.currentDisplayMethod},{data:n,name:e.yName2nd,type:this.$data.currentDisplayMethod}],legend:{orient:"horizontal",x:"center",y:"top"}};this.currentChart.setOption(r,!0)},exportImage:function(){if(this.currentChart){var e=this.currentChart.getDataURL(),t=s(e);Object(i["saveAs"])(t,"chart.png")}}},watch:{currentDisplayMethod:function(){"2nd"===this.typee?this.refreshChart2nd():this.refreshChart()}},computed:{uniqueId:function(){return void 0!==this.uid?this.uid:"globalChart"}},props:["typee","uid"]},u=o,d=a("2877"),c=Object(d["a"])(u,n,r,!1,null,"5ad5f736",null);t["a"]=c.exports},c64a:function(e,t,a){"use strict";a("37d3")},d81d:function(e,t,a){"use strict";var n=a("23e7"),r=a("b727").map,l=a("1dde"),i=a("ae40"),s=l("map"),o=i("map");n({target:"Array",proto:!0,forced:!s||!o},{map:function(e){return r(this,e,arguments.length>1?arguments[1]:void 0)}})},e4af:function(e,t,a){},f70a:function(e,t,a){"use strict";var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("el-form",[a("el-form-item",{attrs:{label:"评价指标表："}},[a("el-table",{attrs:{data:e.tableOneData}},[a("el-table-column",{attrs:{prop:"index",label:"评价指标"}}),a("el-table-column",{attrs:{prop:"r2",label:"R2"}}),a("el-table-column",{attrs:{prop:"mape",label:"MAPE"}}),a("el-table-column",{attrs:{prop:"rmse",label:"RMSE"}})],1)],1),a("el-form-item",[a("el-button",{attrs:{disabled:0===e.tableOneData.length},on:{click:e.exportTableOneSheet}},[e._v("导出评价指标表")])],1),a("el-form-item",{attrs:{label:"年份 − 预测值表："}},[a("el-table",{attrs:{data:e.tableTwoData}},[a("el-table-column",{attrs:{prop:"year",label:"年份"}}),a("el-table-column",{attrs:{prop:"predict",label:"预测值（MVW）"}})],1)],1),a("el-form-item",[a("el-button",{attrs:{disabled:0===e.tableTwoData.length},on:{click:e.exportTableTwoSheet}},[e._v("导出预测结果表")])],1)],1)},r=[],l=a("f59f"),i=a("21a6"),s={name:"ResultTable",data:function(){return{tableOneData:[],tableTwoData:[]}},methods:{exportTableSheet:function(e,t){var a=l["parse"](e,{fields:t}),n=new Blob([a],{type:"text/csv"});Object(i["saveAs"])(n,"database.csv")},exportTableOneSheet:function(){this.exportTableSheet(this.$data.tableOneData,["index","r2","mape","rmse"])},exportTableTwoSheet:function(){this.exportTableSheet(this.$data.tableTwoData,["year","predict"])}}},o=s,u=a("2877"),d=Object(u["a"])(o,n,r,!1,null,"96eed4ac",null);t["a"]=d.exports}}]);
//# sourceMappingURL=chunk-2e87cd74.bfffe175.js.map