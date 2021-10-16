import{d as e,o as s,h as a,B as t,x as o,D as n,b as l,A as r,y as d,s as u,r as m,c as p,w as c,p as g,a as i,f,g as y,z as _,F as v,E as h}from"./vendor.c4bbfea9.js";const b={class:"message_sender"},x={class:"message_text-message"};var w=e({props:{sender:String,message:String,type:String},setup(e){const d=localStorage.getItem("username");return(u,m)=>(s(),a("div",{class:r(e.sender!==l(d)?"member_message":"message_owner")},[t("div",{class:"message",style:n({backgroundColor:e.sender!==l(d)?"#d5d8de":"rgba(24, 160, 88, 0.6)"})},[t("p",b,o(e.sender),1),t("p",x,o(e.message),1)],4)],2))}});g("data-v-c2ff1f90");const k=y("Send message"),S=y("Enter in a room!");i();var C=e({setup(e){const{getters:t}=d(),n=u([]),r=u(""),g="3000"===window.location.host.split(":")[1]?"127.0.0.1:8000":window.location.host,i=t.taskRoom.room_name?t.taskRoom.room_name.replaceAll(" ","_"):null;let b=null;i&&(b=new WebSocket(`ws://${g}/ws/chat/${i}/`),b.onmessage=e=>{const s=JSON.parse(e.data);s.room?s.room.messages.forEach((e=>n.value.push(e))):n.value.push(s)},b.onclose=e=>{console.error("Chat socket closed unexpectedly")});const x=()=>{0!==r.value.trim().length&&b&&(b.send(JSON.stringify({type:"chat_message",sender:localStorage.getItem("username"),message:r.value})),r.value="")};return(e,d)=>{const u=m("n-gradient-text"),g=m("n-h2"),i=m("n-layout-header"),C=m("n-layout"),E=m("n-input"),I=m("n-button"),R=m("n-form"),j=m("n-layout-footer"),z=m("n-space");return l(b)?(s(),p(C,{key:0,style:{height:"90vh"}},{default:c((()=>[f(i,{style:{height:"64px",padding:"24px"},bordered:""},{default:c((()=>[f(g,null,{default:c((()=>[f(u,{size:24,type:"success"},{default:c((()=>[y(o(l(t).taskRoom.room_name),1)])),_:1})])),_:1})])),_:1}),f(C,{position:"absolute",style:{top:"64px",bottom:"64px"},"native-scrollbar":!1},{default:c((()=>[f(C,{"content-style":"padding: 24px;","native-scrollbar":!1},{default:c((()=>[(s(!0),a(v,null,_(n.value,((e,a)=>(s(),p(w,{key:a,sender:e.sender,message:e.message,type:e.type},null,8,["sender","message","type"])))),128))])),_:1})])),_:1}),f(j,{position:"absolute",style:{height:"64px",padding:"24px"},bordered:""},{default:c((()=>[f(R,{class:"message_form"},{default:c((()=>[f(E,{class:"message_input",placeholder:"Type message",value:r.value,"onUpdate:value":d[0]||(d[0]=e=>r.value=e),onKeydown:h(x,["enter"])},null,8,["value","onKeydown"]),f(I,{type:"primary",onClick:x},{default:c((()=>[k])),_:1})])),_:1})])),_:1})])),_:1})):(s(),p(z,{key:1,justify:"center"},{default:c((()=>[f(g,null,{default:c((()=>[S])),_:1})])),_:1}))}}});C.__scopeId="data-v-c2ff1f90";export{C as default};
