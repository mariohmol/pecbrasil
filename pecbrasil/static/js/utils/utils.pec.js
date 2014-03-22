function initChartVars(divId,valor, funcao){
	 $(document.getElementById(divId+'_func_value')).val(funcao);
	 $(document.getElementById(divId+'_depth_value')).val(valor);
}

function getElementByIframeId(iframe,id){
	var iframe = document.getElementById(iframe);
	var innerDoc = (iframe.contentDocument) ? iframe.contentDocument : iframe.contentWindow.document;
	return innerDoc.getElementById(id);
}

function setChartValueFrame(divId,valor){
	
	viz.value(valor);
	setChartFuncFrame(divId,null);
	
	 $(document.getElementById(divId+'_depth_value')).val(valor);
	 if($(document.getElementById(divId+'_func_value')).val()=="media")
		 setChartFuncFrame(divId,null);
	 d3.select('#'+divId).call(viz);
	
}

function setChartYearFrame(divId,valor){
	viz.year(valor); 
	 
	 $(document.getElementById(divId+'_ano_value')).val(valor);
	 setChartFuncFrame(divId,null);
	 d3.select('#'+divId).call(viz);
}

function setChartFuncFrame(divId,valor){
	atualizar=true
	if(valor==null){
		valor = $(document.getElementById(divId+'_func_value')).val();
		atualizar=false
	}
	
	
	var depval = $(document.getElementById(divId+'_depth_value')).val();
	
	if(valor=='media' && depval!=""){
		
		viz.value(depval+"_media");
		
	}else if(valor=='total'){
		
		
		viz.value(depval);	
	}else atualizar=false
	
	if(atualizar){
	 d3.select('#'+divId).call(viz);
	 $(document.getElementById(divId+'_func_value')).val(valor);
	}
	
}

	
function createCandidaturas(attr_candidaturas,partido_partidos)	  {	
	  	 var attrs = {}
	      attr_candidaturas.forEach(function(a){
	        a.candidatura = a.id
	        partido_partidos.forEach(function(p){
		          if(p.id == a.partido){
		          	a.partidoNome = p.name_pt
		          	a.partidoSigla = p.sigla
		          	a.color=p.color
		          }	
	          })	
	          if(politicoid == a.candidatura){
	          
	          	a.color='#000000'
	          }
	        
	       attrs[a.id] = a
	   	})
	   	return attrs;
  }

  function createRodadas(	rodada_rodadas){
	 	var attrsRodada = {}
	   	rodada_rodadas.forEach(function(r){
	   		r.rodada=r.id
	   		attrsRodada[r.id]=r
		})
		return attrsRodada;
  }  	
  

  function createDespesas(despesatipo_despesatipo){
	   	 var attrsDespesa = {}	
	   	despesatipo_despesatipo.forEach(function(a){
		        a.categoria = a.id_despesatipo  
		        attrsDespesa[a.id_despesatipo] = a
   		})
   		return attrsDespesa;
  }
   		
  numeral.language('pt_BR', {
    delimiters: {
        thousands: '.',
        decimal: ','
    },
    abbreviations: {
        thousand: 'k',
        million: 'm',
        billion: 'b',
        trillion: 't'
    },
    ordinal : function (number) {
        return number === 1 ? 'er' : 'ème';
    },
    currency: {
        symbol: 'R$'
    }
});
numeral.language('pt_BR');
$(function() {
	if($(".valorDespesas").length) {

		$(".valorDespesas").each(function() {
			$str = $(this).html();
			$str = numeral($str).format('0,0.00');
			$(this).html($str);
		});
		

	}
	
	$(".actLegenda").click(function(e){
		e.preventDefault();
		$(this).next(".lgn_despesas").slideToggle();
	});
	

	$("div[id^='profile']").each(function(e){
		
		if(e>1&&!$("body").hasClass("home")) { 
			hideToSlideDiv($(this))
		}//else if($("body").hasClass("home")){hideToSlideDiv($(this))}
		
	});

});

function hideToSlideDiv(div){
	div.find('iframe, h4, ul, div, br').hide();
	div.find("h2").click(function(e) {
		e.preventDefault();
		$(this).parent().find('h4, div, br').slideToggle();
		$(this).parent().find("iframe").slideToggle(function(){
			$(".guide_app").not($(this).parent()).not("#profile0").not("#profile2").find("iframe, div, h4, br, ul").slideUp();
			if(!$(this).is(":hidden")) {
				$(this).attr("src", $(this).attr("alt"));
			} else {
				$(this).html("");
			}
		});
	});
}

function addPopUpShare(pid, slug, titleApp,share_url){
	
	pidOriginal=pid
	pid="#"+pid
	d3.select(pid).html("")
	// if (d3.select(pid).empty()) {
         
         dataviva.popover.create({
           "id": "share_info",
           "width": "40%",
           "height": "250px",
           "color": "#fff",
           "close": true
         })
       
       if(window.location != window.parent.location){
         var url = encodeURIComponent(window.parent.location.pathname + window.parent.location.search)
       }
       else {
         var url = encodeURIComponent(window.location.pathname + window.location.search)
       }
       
       
             if(slug=="")slug="data.slug"
           	 if(titleApp=="")titleApp="PoliticaEsporteClube"//"app.viz.title()"
             d3.select(pid).append("h3")
               .text(dataviva.format.text("share_url"))
             
             // make input box with share link
             if(share_url=="") 
             share_url = "http://politicaesporteclube.com"+window.location.pathname ;
             
             d3.select(pid).append("input")
               .attr("type", "text")
               .attr("class", "leon textbox mediumleon textbox large")
               .attr("value", share_url)
               .on(d3plus.evt.click, function(){
                 this.focus();
                 this.select();
               })
             
             d3.select(pid).append("h3")
               .text(dataviva.format.text("embed_url"))
           
             // make input box with embed iframe
             d3.select(pid).append("input")
               .attr("type", "text")
               .attr("class", "leon textbox mediumleon textbox large")
               .attr("value", "<iframe width='560' height='315' src='"+window.location.href+"' frameborder='0'></iframe>")
               .on(d3plus.evt.click, function(){
                 this.focus();
                 this.select();
               })
             
             d3.select(pid).append("h3")
               .text(dataviva.format.text("social_media"))
         
             // Twitter link
             //var share_url = "http://politicaesporteclube.com/"+slug
             d3.select(pid).append("a")
               .attr("href", "https://twitter.com/share?url="+share_url+"&text="+titleApp+"&hashtags=politicaesporteclube")
               .attr("class", "share_button")
               .attr("target", "_blank")
               .attr("onclick", "return !window.open(this.href, 'Twitter', 'width=640,height=300')")
               .attr("id", "Twitter")
               .attr("title", function(){
                 return dataviva.language == "pt" ? "Tweetar" : "Tweet";
               })
             
             // Facebook link
             d3.select(pid).append("a")
             //"&p[url]=http://politicaesporteclube.com/" + slug + "
               .attr("href", "http://www.facebook.com/sharer.php?s=100&p[title]=PoliticaEsporteClube&p[summary]="+titleApp+"&p[url]=" + share_url + "/&p[images][0]=http://politicaesporteclube.com/static/img/pecbrasil/logo-rodape.png")
               .attr("class", "share_button")
               .attr("target", "_blank")
               .attr("onclick", "return !window.open(this.href, 'Facebook', 'width=640,height=300')")
               .attr("id", "Facebook")
               .attr("title", "Facebook")
             
             // Google link
             d3.select(pid).append("a")
               .attr("href", function(){
                 var lang = dataviva.language == "pt" ? "pt-BR" : "en-US";
                 return "https://plus.google.com/share?url=" + share_url + "&hl=" + lang
               })
               .attr("class", "share_button")
               .attr("target", "_blank")
               .attr("onclick", "return !window.open(this.href, 'Google+', 'width=640,height=300')")
               .attr("id", "Google")
               .attr("title", "Google+")
             
	/* } else{
		 //d3.select(pid).html("")
	 } */
 }

/*   
window.addEventListener("message",function(msg){
  d3.select("#app"+msg.data.id.substr(6,1))
    .attr("class",function(){
      var c = this.className.split(" ")
      c[4] = msg.data.app
      return c.join(" ")
    })
    .text(msg.data.title)
})
 */ 
function slide(id) {
  sliding = true
  var id = id.substring(3)
   $("#profile"+id).find("h2").trigger("click");
 
  scroll(id)
}

function load(id) {
	loadRun(id,false)
}

function loadRun(id,run) {
	 
  if (!builds[id].loaded) {
    d3.select("#iframe"+id)
      .attr("src",function(){
        if(run)return this.getAttribute("alt")
      })
    builds[id].loaded = true
  }
}

function select(id) {
  clearInterval(scrollinterval)
  selected = id
  d3.selectAll(".app_links")
    .attr("class",function(){
      if (this.id.substring(3) == id) return this.className.replace("help","decision")
      else return this.className.replace("decision","help")
    })
}

function scroll(id) {
  
  select(id)

  var position = builds[id].top,
      start = window.pageYOffset,
      difference = position - start,
      ticks = 50
      
  var i = 0
  
  function scrollto(){
    var val = Math.easeInOutCubic(i,start,difference,ticks)
    window.scrollTo(0,val)
    
    i++
    if (i == ticks) {
      window.scrollTo(0,position)
      load(id)
      clearInterval(scrollinterval)
      setTimeout(function(){
        sliding = false
      },1000)
    }
  }
  
  scrollinterval = setInterval(scrollto,10)

}

Math.easeInOutCubic = function (t, b, c, d) {
	t /= d/2;
	if (t < 1) return c/2*t*t*t + b;
	t -= 2;
	return c/2*(t*t*t + 2) + b;
}

function initSlides(){
	if (Object.keys(builds).length > 1) {
	  document.onscroll = function() {
	    if (!sliding) {
	      var page = window.pageYOffset
	      for (b in builds) {
	        if(page < ((builds[2].top*(b))-20) && page > ((builds[2].top*(b-2))+20)) {
	          if (page+(builds[2].top/2) < builds[b].top+builds[2].top
	              && page+(builds[2].top/2) > builds[b].top && selected != b) {
	                select(b)
	              }
	          if (!builds[b].loaded) load(b)
	        }
	      }
	    }
	  }
	
	  document.onkeydown = function(e) {
	    var trans = null
	    if (e.keyCode == 34 || e.keyCode == 39 || e.keyCode == 40) { 
	      if (selected < Object.keys(builds).length) trans = parseInt(selected)+1
	      else trans = selected
	    }
	    else if (e.keyCode == 33 || e.keyCode == 37 || e.keyCode == 38) { 
	      if (selected > 1) trans = parseInt(selected)-1
	      else trans = selected
	    }
	    else if (e.keyCode == 36) { 
	      trans = 1
	    }
	    else if (e.keyCode == 35) { 
	      trans = Object.keys(builds).length
	    }
	  
	    if (trans) slide("app"+trans)
	  };
	}
}