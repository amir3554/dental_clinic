$(document).ready(function(){

$('.datepicker').datepicker({
    format: 'dd-mm-yyyy',
    autoclose: true,
    startDate: '0d'
});

$('.cell').click(function(){
    $('.cell').removeClass('select');
    $(this).addClass('select');
});

});


$(function(){
  // 1) عندما يختار المستخدم التاريخ
  $('#dp1').datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true,
    todayHighlight: true
  }).on('changeDate', function(e){
    // بعد اختيار اليوم نضعه في الحقل المخفي
    $('#hidden_date').val( $(this).val() );
  });

  // 2) إذا عندك شبكة أوقات clickable، نلتقط نقرات المستخدم على الخلية
  $('.cell').on('click', function(){
    // إزالة تحديد العنصر السابق
    $('.cell.selected').removeClass('selected');
    // تمييز العنصر الحالي
    $(this).addClass('selected');
    // قراءة التاريخ من الـ datepicker
    const datePart = $('#dp1').val();
    // قراءة الوقت من نصّ الخلية
    const timePart = $(this).text().trim();
    
    // دمج التاريخ والوقت بالشكل الذي يناسب موديلك
    $('#hidden_date').val( datePart + ' ' + timePart );
  });

  // 3) للتأكيد قبل الإرسال:  
  //    لو المستخدم لم يضغط على أي خانة زمنية، نعطيه تحذير
  $('#appointmentForm').on('submit', function(){
    if (!$('#hidden_date').val()) {
      alert('رجاءً اختر التاريخ والوقت أولاً');
      return false; // يمنع الإرسال
    }
  });
});

