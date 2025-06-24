
// // دالة بسيطة لجلب قيمة الـ CSRF من الكوكيز
// function getCookie(name) {
// let cookieValue = null;
// if (document.cookie && document.cookie !== '') {
//     document.cookie.split(';').forEach(cookie => {
//     let [key, val] = cookie.trim().split('=');
//     if (key === name) cookieValue = decodeURIComponent(val);
//     });
// }
// return cookieValue;
// }

// function makeAppointment (aid) {
//     const card = document.getElementById(`operation-${aid}`)

//     const dateInput = card.querySelector('.operation-date');
//     const datetime    = dateInput.value; //YYYY-MM-DDTHH:MM

//      // نبني جسم الرسالة
//     const payload = {
//         operation_id: aid,
//         datetime: datetime
//     };

//     // 2. أرسل إلى السيرفر عبر fetch (POST)
//     fetch('/clinic/appointment/make/', {
//         method: 'POST',
//         headers: {
//         'Content-Type': 'application/json',
//         'X-CSRFToken': getCookie('csrftoken')  // ضروري في Django
//         },
//         body: JSON.stringify(payload)
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('خطأ في الحجز');
//         return response.json();
//     })
//     .then(data => {
//         // مثلاً توجه المستخدم إلى صفحة التأكيد
//         window.location.href = `/appointments/${data.appointment_id}/detail/`;
//     })
//     .catch(err => {
//         console.error(err);
//         alert('تعذّر إجراء الحجز، حاول مجدداً');
//     });
// }
