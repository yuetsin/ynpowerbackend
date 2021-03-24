(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-01945709"],{"21c9":function(e,a,t){"use strict";var n=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("el-row",{style:e.mainStyle,attrs:{type:"flex",justify:"left"}},[t("el-col",[t("el-date-picker",{attrs:{type:"year",placeholder:"起始年份"},on:{change:e.beginChange},model:{value:e.beginYearInternal,callback:function(a){e.beginYearInternal=a},expression:"beginYearInternal"}})],1),t("el-col",{staticStyle:{margin:"auto","text-align":"center",color:"lightgray","font-size":"12px"}},[e._v(" 至 ")]),t("el-col",[t("el-date-picker",{attrs:{type:"year",placeholder:"终止年份"},on:{change:e.endChange},model:{value:e.endYearInternal,callback:function(a){e.endYearInternal=a},expression:"endYearInternal"}})],1)],1)},r=[],l={name:"YearRangeSelector",props:["beginYear","endYear","expand"],data:function(){return{beginYearInternal:this.beginYear,endYearInternal:this.endYear}},methods:{beginChange:function(e){null===e?this.$emit("update:beginYear",null):this.$emit("update:beginYear",e.getFullYear())},endChange:function(e){null===e?this.$emit("update:endYear",null):this.$emit("update:endYear",e.getFullYear())}},watch:{beginYearInternal:function(e){null!==e?this.$emit("update:beginYear",e.getFullYear()):this.$emit("update:beginYear",null)},endYearInternal:function(e){null!==e?this.$emit("update:endYear",e.getFullYear()):this.$emit("update:endYear",null)},beginYear:function(e){this.beginYearInternal=null!==e?new Date(e,1,1):null},endYear:function(e){this.endYearInternal=null!==e?new Date(e,1,1):null}},computed:{mainStyle:function(){return this.expand?"":"width: 55%"}}},i=l,o=(t("6e83"),t("2877")),s=Object(o["a"])(i,n,r,!1,null,"7bfa7c13",null);a["a"]=s.exports},"6e83":function(e,a,t){"use strict";t("e4af")},7939:function(e,a,t){"use strict";t("d827")},"860d":function(e,a,t){"use strict";t.r(a);var n=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("el-row",[t("el-col",{attrs:{span:8,offset:1}},[t("el-form",[t("el-form-item",{attrs:{label:"数据节点："}},[t("el-cascader",{ref:"cascader",attrs:{id:"cascader",options:e.metaDataTree,"change-on-select":""},model:{value:e.postParams.category,callback:function(a){e.$set(e.postParams,"category",a)},expression:"postParams.category"}})],1),t("el-form-item",{attrs:{label:"地区选择："}},[t("el-select",{attrs:{placeholder:"请选择"},model:{value:e.postParams.region,callback:function(a){e.$set(e.postParams,"region",a)},expression:"postParams.region"}},e._l(e.knownRegions,(function(e){return t("el-option",{key:e,attrs:{label:e,value:e}})})),1)],1),t("el-form-item",{attrs:{label:"粒度选择："}},[t("el-select",{attrs:{placeholder:"请选择"},model:{value:e.postParams.grain,callback:function(a){e.$set(e.postParams,"grain",a)},expression:"postParams.grain"}},e._l(e.knownGrains,(function(e){return t("el-option",{key:e,attrs:{label:e,value:e}})})),1)],1),t("el-form-item",{attrs:{label:"年份选择："}},[t("year-range-selector",{attrs:{"begin-year":e.postParams.beginYear,"end-year":e.postParams.endYear},on:{"update:beginYear":function(a){return e.$set(e.postParams,"beginYear",a)},"update:begin-year":function(a){return e.$set(e.postParams,"beginYear",a)},"update:endYear":function(a){return e.$set(e.postParams,"endYear",a)},"update:end-year":function(a){return e.$set(e.postParams,"endYear",a)}}})],1),t("el-form-item",[t("el-button",{attrs:{disabled:null===e.postParams.beginYear||null===e.postParams.endYear||0===e.postParams.category.length},on:{click:e.loadExceptions}},[e._v(" 异常检测 ")])],1)],1)],1),t("el-col",{attrs:{span:15}},[t("data-patch-table",{attrs:{"display-data":e.tableData}})],1)],1)},r=[],l=function(){var e=this,a=e.$createElement,t=e._self._c||a;return t("div",[t("d2-crud",{ref:"d2Crud",attrs:{columns:e.columns,data:e.displayData,rowHandle:e.rowHandle,"edit-template":e.editTemplate},on:{"dialog-cancel":e.handleDialogCancel,"row-edit":e.handleRowResolve,"row-remove":e.handleRowAccept}}),t("div",{staticStyle:{color:"darkgray","font-size":"12px"}},[e._v(" 共 "+e._s(e.dataEntryLength)+" 条 ")])],1)},i=[],o={name:"DataPatchTable",props:["displayData"],computed:{dataEntryLength:function(){return void 0===this.displayData?0:this.displayData.length}},data:function(){return{columns:[{title:"元数据类型",key:"category"},{title:"数据粒度",key:"grain"},{title:"地区",key:"region"},{title:"键",key:"key"},{title:"当前值",key:"value"},{title:"更正建议",key:"suggest"}],editTemplate:{key:{title:"键"},value:{title:"值"}},rowHandle:{remove:{text:"接受",size:"small",type:"primary",confirm:!1},edit:{text:"更正",size:"small",fixed:"right"}}}},methods:{handleDialogCancel:function(e){e()},handleRowResolve:function(e,a){var t=this,n=e.index,r=e.row;this.$axios.post("/db/except/resolve",{originData:this.displayData[n],modifiedData:r}).then((function(e){console.log(e),t.$messenger.success("手动更正成功。"),t.displayData.remove(n),a()}))},handleRowAccept:function(e,a){var t=this,n=e.index;e.row;this.$axios.post("/db/except/accept",{acceptData:this.displayData[n]}).then((function(e){console.log(e),t.$messenger.success("已接受更正建议。"),t.displayData.remove(n),a()}))}}},s=o,c=t("2877"),d=Object(c["a"])(s,l,i,!1,null,"7a0e21a4",null),u=d.exports,p=t("21c9"),g={name:"dataCheck",components:{YearRangeSelector:p["a"],DataPatchTable:u},data:function(){return{tableData:[],metaDataTree:[],knownRegions:[],knownGrains:[],postParams:{category:[],region:null,grain:null,beginYear:null,endYear:null}}},mounted:function(){this.loadMetaData(),this.loadRegions(),this.loadGrains()},methods:{loadMetaData:function(){var e=this;this.$axios.get("/db/metadata").then((function(a){e.$data.metaDataTree=a.data.data}))},loadExceptions:function(){var e=this;this.$axios.post("/db/except/query",this.$data.postParams).then((function(a){e.tableData=a.data.data}))},loadRegions:function(){var e=this;this.$axios.get("/region/query").then((function(a){e.$data.knownRegions=a.data.data}))},loadGrains:function(){var e=this;this.$axios.get("/grain/query").then((function(a){e.$data.knownGrains=a.data.data}))}}},m=g,h=(t("7939"),Object(c["a"])(m,n,r,!1,null,"510aac02",null));a["default"]=h.exports},d827:function(e,a,t){},e4af:function(e,a,t){}}]);
//# sourceMappingURL=chunk-01945709.ca5fc67e.js.map