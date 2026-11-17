(function(){var D=[["l","p01.html","读后赞言（代序）"],["l","p02.html","对我国今后几十年人口发展战略的几点意见"],["l","p03.html","中国人口变动五十年展望"],["l","p04.html","关于我国人口老化的趋势和对劳动资源问题的分析"],["l","p05.html","关于我国人口老化的几个问题"],["l","p06.html","也谈我国人口发展目标"],["l","p07.html","论人口目标对社会经济结构的影响"],["l","p08.html","对我国人口学发展的几个问题的认识"],["l","p09.html","关于“适中人口”"],["l","p10.html","世界新的技术革命和我国人口对策"],["l","p11.html","把计划生育工作建立在人口发展规律的基础上"],["l","p12.html","答新华社记者问"],["l","p13.html","论我国农村人口发展战略"],["l","p14.html","关于我国人口发展战略的几个问题"],["l","p15.html","校后记"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
