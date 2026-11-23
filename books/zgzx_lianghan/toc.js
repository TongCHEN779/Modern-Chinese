(function(){var D=[["l","p01.html","编辑说明"],["l","p02.html","董仲舒"],["l","p03.html","淮南子"],["l","p04.html","司马迁"],["l","p05.html","扬雄"],["l","p06.html","桓谭"],["l","p07.html","王充"],["l","p08.html","仲长统"],["l","p09.html","何晏"],["l","p10.html","王弼"],["l","p11.html","嵇康"],["l","p12.html","杨泉"],["l","p13.html","欧阳建"],["l","p14.html","裴頠"],["l","p15.html","向秀 郭象"],["l","p16.html","鲍敬言"],["l","p17.html","列子"],["l","p18.html","僧肇"],["l","p19.html","何承天"],["l","p20.html","范缜"],["l","p21.html","吕才"],["l","p22.html","玄奘"],["l","p23.html","慧能"],["l","p24.html","韩愈"],["l","p25.html","李翱"],["l","p26.html","柳宗元"],["l","p27.html","刘禹锡"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
