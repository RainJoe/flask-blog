webpackJsonp([1],{Wwud:function(t,e,o){var n=o("bDpX");"string"==typeof n&&(n=[[t.i,n,""]]),n.locals&&(t.exports=n.locals);o("rjj0")("a1f3ed80",n,!0)},bDpX:function(t,e,o){(t.exports=o("FZ+f")(void 0)).push([t.i,".post-wrapper{margin-top:40px}",""])},"us+q":function(t,e,o){"use strict";var n=o("mtWM"),a=o.n(n),s={data:function(){return{open:!1,value:"1",value2:"1",avatar:window.sessionStorage.getItem("avatar"),login:window.sessionStorage.getItem("key"),body:"",articles:""}},props:["posts"],methods:{toggle:function(){this.open=!this.open},logout:function(){var t=this;t.login=!1,window.sessionStorage.removeItem("key"),window.sessionStorage.removeItem("admin"),window.sessionStorage.removeItem("avatar"),a()({method:"DELETE",url:"/sessions",headers:{"Content-Type":"application/json"}}).then(function(e){t.$router.push({name:"HelloWorld"})}).catch(function(t){console.log(t)})},handleChange:function(t){this.value===t&&this.logout()},handleChange2:function(t){t!=this.value2&&this.$router.push({name:"Detail",params:{id:t}})},fetchData:function(){var t=this;"Detail"===t.$route.name&&a()({method:"GET",url:"/posts",headers:{"Content-Type":"application/json"}}).then(function(e){t.articles=e.data.posts}).catch(function(t){console.log(t)})}},mounted:function(){this.fetchData()}},i={render:function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",[o("mu-appbar",[o("router-link",{attrs:{to:"/"},nativeOn:{click:function(e){t.back()}}},[t._v("Rare")]),t._v(" "),o("mu-icon-button",{attrs:{slot:"left",icon:"menu"},on:{click:function(e){t.toggle()}},slot:"left"}),t._v(" "),o("mu-avatar",{directives:[{name:"show",rawName:"v-show",value:t.login,expression:"login"}],attrs:{slot:"right",src:t.avatar},slot:"right"}),t._v(" "),o("mu-icon-menu",{directives:[{name:"show",rawName:"v-show",value:t.login,expression:"login"}],attrs:{slot:"right",icon:"more_vert"},on:{change:t.handleChange},slot:"right"},[o("mu-menu-item",{attrs:{value:"1",title:"退出登录"},on:{click:t.logout}})],1)],1),t._v(" "),o("mu-drawer",{attrs:{left:"",open:t.open,docked:!1},on:{close:function(e){t.toggle()}}},[o("mu-appbar",{attrs:{title:"Rare"}}),t._v(" "),o("mu-list",{attrs:{value:t.value2},on:{change:t.handleChange2}},[o("mu-list-item",{attrs:{open:!1,value:1,title:"文章",inset:"",toggleNested:""}},[o("mu-icon",{attrs:{slot:"left",value:"grade"},slot:"left"}),t._v(" "),t._l(t.posts?t.posts:t.articles,function(t){return o("mu-list-item",{key:t.id,attrs:{slot:"nested",value:t.id,title:t.title},slot:"nested"})})],2)],1)],1)],1)},staticRenderFns:[]},r=o("VU/8")(s,i,!1,null,null,null);e.a=r.exports},wHgX:function(t,e,o){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=o("mtWM"),a=o.n(n),s={data:function(){return{value:"1",avatar:window.sessionStorage.getItem("avatar"),login:window.sessionStorage.getItem("key"),body:"",comments:"",commentBody:""}},methods:{logout:function(){var t=this;t.login=!1,window.sessionStorage.removeItem("key"),window.sessionStorage.removeItem("admin"),window.sessionStorage.removeItem("avatar"),a()({method:"DELETE",url:"/sessions",headers:{"Content-Type":"application/json"}}).then(function(e){t.$router.push({name:"HelloWorld"})}).catch(function(t){console.log(t)})},toLogin:function(){this.$router.push({name:"Login"})},handleChange:function(t){this.value===t&&this.logout()},fetchPost:function(t){var e=this;a()({method:"GET",url:"posts/"+t,headers:{"Content-Type":"application/json"}}).then(function(t){e.body=t.data.body}).catch(function(t){console.log(t)})},fetchComment:function(t){var e=this;a()({method:"GET",url:"comments/"+t,headers:{"Content-Type":"application/json"}}).then(function(t){e.comments=t.data}).catch(function(t){console.log(t)})},fetchData:function(t){this.fetchPost(t),this.fetchComment(t)},submitForm:function(){var t=this;this.commentBody?a()({url:"/comments/"+this.$route.params.id,method:"POST",headers:{Authorization:window.sessionStorage.getItem("key"),"Content-Type":"application/json"},data:{body:this.commentBody}}).then(function(e){t.fetchComment(t.$route.params.id)}).catch(function(t){console.log(t)}):alert("评论不能为空")}},mounted:function(){this.fetchData(this.$route.params.id)},components:{appbar:o("us+q").a},watch:{$route:function(t,e){this.fetchData(this.$route.params.id)}}},i={render:function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",[o("appbar"),t._v(" "),o("div",{staticClass:"post-wrapper"},[o("mu-row",[o("mu-col",{attrs:{width:"0",tablet:"15",desktop:"25"}}),t._v(" "),o("mu-col",{attrs:{width:"100",tablet:"70",desktop:"50"}},[o("mu-content-block",[o("div",{directives:[{name:"highlight",rawName:"v-highlight"}],domProps:{innerHTML:t._s(t.body)}})]),t._v(" "),o("div",{staticClass:"comment-wrapper"},[o("mu-list",t._l(t.comments,function(e){return o("div",{key:e.id},[o("mu-list-item",{attrs:{title:e.author_name}},[o("mu-avatar",{attrs:{slot:"leftAvatar",src:e.author_avatar},slot:"leftAvatar"}),t._v(" "),o("span",{attrs:{slot:"describe"},slot:"describe"},[o("span",{staticStyle:{color:"rgba(0, 0, 0, .87)"}},[t._v(t._s(t._f("moment")(e.created_time)))])]),t._v(" "),o("p",[t._v(t._s(e.body))])],1),t._v(" "),o("mu-divider",{attrs:{inset:""}})],1)})),t._v(" "),o("mu-text-field",{attrs:{hintText:"评论",multiLine:"",rows:3,fullWidth:""},model:{value:t.commentBody,callback:function(e){t.commentBody=e},expression:"commentBody"}}),o("br"),t._v(" "),o("mu-raised-button",{directives:[{name:"show",rawName:"v-show",value:t.login,expression:"login"}],staticClass:"demo-raised-button",attrs:{label:"提交"},on:{click:t.submitForm}}),t._v(" "),o("mu-raised-button",{directives:[{name:"show",rawName:"v-show",value:!t.login,expression:"!login"}],staticClass:"demo-raised-button",attrs:{label:"登录后才能评论"},on:{click:t.toLogin}})],1)],1),t._v(" "),o("mu-col",{attrs:{width:"0",tablet:"15",desktop:"25"}})],1)],1)],1)},staticRenderFns:[]},r=o("VU/8")(s,i,!1,function(t){o("Wwud")},null,null);e.default=r.exports}});
//# sourceMappingURL=1.846c031f5c25d7acab1b.js.map