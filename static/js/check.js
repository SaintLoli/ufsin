let count = 0;

function validateForm(event) {
    event.preventDefault();

    const gpu = document.getElementById('gpu').value;
    const cpu = document.getElementById('cpu').value;
    const motherboard = document.getElementById('motherboard').value;
    const year = document.getElementById('year').value;
    const ram = document.getElementById('ram').value;
    const sNumber = document.getElementById('s_number').value;

    let devicesHTML = '';
    let localCount = 1;

    const deviceFields = document.querySelectorAll('.device-fields');
    deviceFields.forEach(device => {
        const type = device.querySelector('.device-type').value;
        const name = device.querySelector('.device-name').value;
        const serial = device.querySelector('.device-serial').value;
        const deviceYear = device.querySelector('.device-year').value;
        devicesHTML += `
            <h4 align="center">Устройство ${localCount}</h4>
            <li class="list-group-item"><strong>Тип устройства:</strong> ${type}</li>
            <li class="list-group-item"><strong>Название:</strong> ${name}</li>
            <li class="list-group-item"><strong>Серийный номер:</strong> ${serial}</li>
            <li class="list-group-item"><strong>Год выпуска:</strong> ${deviceYear}</li>
        `;
        localCount++;
    });

    const resultsHTML = `
        <ul class="list-group">
            <li class="list-group-item"><strong>GPU:</strong> ${gpu}</li>
            <li class="list-group-item"><strong>CPU:</strong> ${cpu}</li>
            <li class="list-group-item"><strong>Материнская плата:</strong> ${motherboard}</li>
            <li class="list-group-item"><strong>Год выпуска:</strong> ${year}</li>
            <li class="list-group-item"><strong>ОЗУ:</strong> ${ram} ГБ</li>
            <li class="list-group-item"><strong>Серийный номер ПК:</strong> ${sNumber}</li>
            ${devicesHTML}
        </ul>
    `;

    document.getElementById('checkResults').innerHTML = resultsHTML;
    document.getElementById('checkForm').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Собираем данные формы
    const formData = new FormData();
    formData.append('cpu', cpu);
    formData.append('motherboard', motherboard);
    formData.append('gpu', gpu);
    formData.append('ram', ram);
    formData.append('year', year);
    formData.append('s_number', sNumber);

    // Добавляем устройства в форму
    deviceFields.forEach((device, index) => {
        formData.append(`device_type_${index + 1}`, device.querySelector('.device-type').value);
        formData.append(`device_name_${index + 1}`, device.querySelector('.device-name').value);
        formData.append(`device_s_number_${index + 1}`, device.querySelector('.device-serial').value);
        formData.append(`device_year_${index + 1}`, device.querySelector('.device-year').value);
    });

    // Отправляем данные через fetch
    fetch('/pc_register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Ошибка отправки:', error);
    });

    return false
}

function resetForm() {
    document.getElementById('checkForm').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function endChanges() {
//    document.getElementById("endChanges").submit();
    resetForm()
}
