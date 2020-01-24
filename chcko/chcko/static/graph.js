/*jshint unused:false */
/*global functions:true */

function axis(scale,po)
{
    this.po = po;
    this.scale = scale;
    this.pos = function(n)
    {
        return this.po+this.scale*n;
    };
    this.num = function(p)
    {
        return (p-this.po)/this.scale;
    };
}

function CS2dims(nr,divname)
{
    this.colors = [
        "rgb(0,153,0)",
        "rgb(204,0,204)",
        "rgb(153,153,255)",
        "rgb(0,255,0)"
        ];
    var contentdiv = document.getElementById(divname);
    if (contentdiv === null)
    {
        return;
    }
    this.canvas = document.createElement("canvas");
    this.canvas.id = "canvas"+nr;
    this.canvas.width = 402;
    this.canvas.height = 402;
    contentdiv.appendChild(this.canvas);
    if (null===this.canvas || !this.canvas.getContext)
    {
        return;
    }
    var w=this.canvas.width;
    var h=this.canvas.height;
    this.context = this.canvas.getContext("2d");
    this.axes =
    {
       x: new axis(40,0.5+0.5*w),
       y: new axis(-40,0.5+0.5*h)
    };
    var xx = this.axes.x;
    var yy = this.axes.y;
    var xMin = xx.num(0);
    var xMax = xx.num(w);
    var yMin = yy.num(h);
    var yMax = yy.num(0);

    var x,y,px,py,v;
    var px0=this.axes.x.po;
    var py0=this.axes.y.po;
    this.showAxes=function()
    {
        this.context.beginPath();
        this.context.strokeStyle = "rgb(128,128,128)";
        this.context.moveTo(0,py0); this.context.lineTo(w,py0);
        this.context.moveTo(px0,0); this.context.lineTo(px0,h);
        var fontsz = 10;
        this.context.font = fontsz.toString+"px sans-serif";
        var tl = 5;
        this.context.textAlign="center";
        for (x = xMin; x<xMax; x=x+1)
        {
            px = xx.pos(x);
            v=Math.round(x);
            if (v===0)
            {
                continue;
            }
            this.context.moveTo(px,py0-tl);
            this.context.lineTo(px,py0+tl);
            this.context.strokeText(v.toString(),px,py0+tl+fontsz);
        }
        this.context.textAlign="right";
        for (y = yMin; y<yMax; y=y+1)
        {
            py = yy.pos(y);
            v=Math.round(y);
            if (v===0)
            {
                continue;
            }
            this.context.moveTo(px0-tl,py);
            this.context.lineTo(px0+tl,py);
            this.context.strokeText(v.toString(),px0-tl-fontsz/2,py+fontsz/2);
        }
        this.context.stroke();
    };

    this.show = function(func,color,thick)
    {
        var pyo;
        var dx = xx.num(3)-xMin;
        this.context.beginPath();
        this.context.lineWidth = thick;
        this.context.strokeStyle = this.colors[color];
        var cpx=15,cpy=20;
        for (x=xMin;x<=xMax;x+=dx)
        {
            pyo = py;
            px = xx.pos(x);
            py = yy.pos(func(x));
            if ( py === Infinity || py === -Infinity )
            {
                px = xx.pos(x)+1;
                x = yy.num(px);
                y = func(x);
                py = yy.pos(x);
            }
            if (x===xMin ||
            (py<0 && pyo>h)||
            (pyo<0 && py>h))
            {
                this.context.moveTo(px,py);
            }
            else
            {
                this.context.lineTo(px,py);
            }
            if (px > 15 && px < w-15 && py > 20 && py < h-20)
            {
                cpx = px;
                cpy = py;
            }
        }
        this.context.stroke();
        return [cpx,cpy];
    };
}

var thiscF;
var thisCS;

function createCS(nr,divname)
{
    thisCS = new CS2dims(nr,divname);
    thisCS.showAxes();
    return thisCS;
}

var clr = 0;
function drawFunc()
{
    var p={};
    for (var paramName in thiscF.params){
    if (paramName) {
        var ip = document.getElementById(paramName);
        if (ip)
        {
            var f = parseFloat(ip.value);
            if (isNaN(f))
            { return;}
            p[paramName]=f;
        }
    }}
    clr = (clr+1)%4;
    thisCS.show(thiscF.createfunc(p),clr,1);
}

var redraw;

function setCurrent(e)
{
    if (e.target.checked)
    {
        thiscF = functions[e.target.value][0];
    }
    var radiodiv = document.getElementById('radiodiv');
    if (radiodiv)
    {
        var spaceforparams = document.getElementById('params');
        if (spaceforparams)
        {
            spaceforparams.parentNode.removeChild(spaceforparams);
        }
        spaceforparams = document.createElement('div');
        spaceforparams.id = 'params';
        var tbl = document.createElement('table');
        for (var paramName in thiscF.params){
        if (paramName) {
            var tr = document.createElement('tr');
            var td = document.createElement('td');
            td.innerHTML = paramName;
            td.style.border = "0px";
            tr.appendChild(td);
            td = document.createElement('td');
            td.style.border = "0px";
            var nb = document.createElement('input');
            nb.type = "number";
            nb.id = paramName;
            var pp = thiscF.params[paramName];
            nb.value = pp[0];
            nb.innerHTML = pp[0];
            nb.min = pp[1];
            nb.max = pp[2];
            nb.step = pp[3];
            nb.onchange = drawFunc;
            td.appendChild(nb);
            tr.appendChild(td);
            tbl.appendChild(tr);
        }}
        spaceforparams.appendChild(tbl);
        redraw = document.createElement('button');
        redraw.innerHTML = "-1-";
        redraw.id = "-1-";
        redraw.onclick = function(){thisCS.canvas.width=thisCS.canvas.width; thisCS.showAxes();drawFunc();};
        spaceforparams.appendChild(redraw);
        radiodiv.appendChild(spaceforparams);
    }
}

function fillFields(radio,fields)
{
    var aradio = document.getElementById(radio);
    if (aradio)
    {
        aradio.checked = true;
        var e={target:aradio};
        setCurrent(e);
        for (var f in fields){
        if (fields.hasOwnProperty(f))
        {
            var ff = document.getElementById(fields[f][0]);
            if (ff)
            {
                ff.value = fields[f][1];
            }
        }}
        if (redraw)
        {
            e={target:redraw};
            redraw.onclick.apply(e);
        }
    }
}

function createRadios(divname)
{
    if (functions)
    {
        var contentdiv = document.getElementById(divname);
        if (contentdiv)
        {
            var radiodiv = document.getElementById('radiodiv');
            if (radiodiv)
            {
                radiodiv.parentNode.removeChild(radiodiv);
            }
            radiodiv = document.createElement('div');
            radiodiv.id = "radiodiv";
            radiodiv.setAttribute("class","divleft");
            radiodiv.style.width = "40%";
            contentdiv.appendChild(radiodiv);
            for (var funtype in functions){
            if (functions.hasOwnProperty(funtype)){
                var lbl = document.createElement("label");
                lbl.innerHTML = funtype;
                radiodiv.appendChild(lbl);
                radiodiv.appendChild(document.createElement("br"));
                var aradio = document.createElement("input");
                aradio.type = "radio";
                aradio.id = funtype;
                aradio.value=funtype;
                aradio.name = "functype";
                aradio.onclick = setCurrent;
                radiodiv.appendChild(aradio);
                lbl = document.createElement("label");
                lbl.innerHTML = functions[funtype][1];
                radiodiv.appendChild(lbl);
                radiodiv.appendChild(document.createElement("br"));
            }}
        }
    }
}




