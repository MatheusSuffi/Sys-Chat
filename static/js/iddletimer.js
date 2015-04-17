$(document).ready(function(){

   $.get("{{=URL(a='teste_chat', c='home', f='usuarios_online')}}",function(data){
        $('#usuario_online').html(data);
    });
    var data;
    $.web2py.web2py_websocket('ws://localhost:8888/realtime/conversa',function(e){
        $.get("{{=URL(a='teste_chat', c='home', f='usuarios_online')}}",function(data){
            $('#usuario_online').html(data);
        });
    ;});
    $('#novaPublicacao').click(function(){
        if($('#texto_mensagem').val() != ''){
            $.get("{{=URL(a='teste_chat', c='home', f='nova_publicacao')}}?mensagem="+$('#texto_mensagem').val(),function(data){     
                $('#linha_tempo').html(data);
            });
        };
    });

});
    $( document ).idleTimer( 10000 );

$(function() {
    $( document ).on( "idle.idleTimer", function(event, elem, obj){
        // function you want to fire when the user goes idle
    });








$(function() {
    $( document ).on( "idle.idleTimer", function(event, elem, obj){
        // function you want to fire when the user goes idle
    });
