$(function () {
    var canvas = this.__canvas = new fabric.Canvas('c', {
        isDrawingMode: true
        });
    canvas = window._canvas = new fabric.Canvas('canvas');
    canvas.backgroundColor = '#efefef';
    canvas.isDrawingMode= 1;
    canvas.freeDrawingBrush.color = "purple";
    canvas.freeDrawingBrush.width = 10;
    canvas.renderAll();

    document.getElementById('colorpicker').addEventListener('click', function (e) {
        console.log(e.target.value);
        canvas.freeDrawingBrush.color = e.target.value;
    });

});

function myFunction() {
    console.log("hahah");
    document.getElementById('hidden').value = canvas.toDataURL();
    document.forms["form1"].submit();
}