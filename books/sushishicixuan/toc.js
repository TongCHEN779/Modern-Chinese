(function(){var D=[["g","苏轼诗选"],["l","p01.html","前言"],["l","p02.html","再版告读者"],["l","p03.html","初发嘉州—寄题兴州晁太守新开古东池"],["l","p04.html","石苍舒醉墨堂—吴中田妇叹"],["l","p05.html","冬至日独游吉祥寺—夜至永乐文长老院，文时卧病退院"],["l","p06.html","过永乐文长老已卒—宿州次韵刘泾"],["l","p07.html","次韵答邦直子由—月夜与客饮杏花下"],["l","p08.html","泗州僧伽塔—和秦太虚梅花"],["l","p09.html","海棠—书李世南所画秋景二首"],["l","p10.html","书鄢陵王主簿所画折枝二首—书晁说之《考牧图》后"],["l","p11.html","雪浪石—送别"],["g","苏轼词选"],["l","p12.html","词选前言"],["l","p13.html","行香子·过七里濑—江城子·密州出猎"],["l","p14.html","望江南·超然台作—一丛花·初春病起"],["l","p15.html","满庭芳·有王长官者—减字木兰花·己卯儋耳春词"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
