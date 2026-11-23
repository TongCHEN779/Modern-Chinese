(function(){var D=[["l","p01.html","“西方古典学研究”总序"],["l","p02.html","导读"],["l","p03.html","Series Editor&#x27;s Introduction"],["l","p04.html","Volume Editor&#x27;s Introduction"],["l","p05.html","Abbreviations"],["l","p06.html","Symbols"],["g","史料译注"],["l","p07.html","Chapter 1 FROM IPSOS TO KORUPEDION (301-281)"],["l","p08.html","Chapter 2 THE SELEUCID KINGDOM"],["l","p09.html","Chapter 3 THE GREEKS IN BAKTRIA AND INDIA"],["l","p10.html","Chapter 4 MACEDON AND THE GREEKS OF EUROPE"],["l","p11.html","Chapter 5 PERGAMON"],["l","p12.html","Chapter 6 PTOLEMAIC EGYPT: KINGDOM AND EMPIRE"],["l","p13.html","Glossary"],["l","p14.html","Appendix"]];var t=document.querySelector('.toc.side');if(!t)return;var ul=t.querySelector('ul'),cur=t.getAttribute('data-cur'),tp=t.querySelector('template');
D.forEach(function(d){var li=document.createElement('li');
if(d[0]==='g'){li.className='grp';li.textContent=d[1];}
else if(d[0]==='x'){var s=document.createElement('span');s.textContent=d[1];li.appendChild(s);}
else{var a=document.createElement('a');a.href=d[1];a.innerHTML=d[2];li.appendChild(a);
if(d[1]===cur){li.className='cur';a.setAttribute('aria-current','page');if(tp)li.appendChild(tp.content.cloneNode(true));}}
ul.appendChild(li);});})();
