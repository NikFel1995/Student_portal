const url = window.location.href
const timerBox = document.getElementById('timer-box')
const endBtn = document.getElementById('end-button')

$.ajax({
    type: 'GET',
    url: `${url}data/`,
    success: function (response) {
        activateTimer(response.time)
    },
    error: function (error) {
    }
});


const activateTimer = (time) => {
    timerBox.innerHTML = `<b>Время пошло ...</b>`

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }

        if (minutes == 0 && seconds <= 59) {
            if (timerBox.classList.contains('alert-primary'))
                timerBox.classList.remove('alert-primary')
            if (!timerBox.classList.contains('alert-danger'))
                timerBox.classList.add('alert-danger')
        }

        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(() => {
                clearInterval(timer)
                alert('Время вышло!')
                endBtn.click()
                // sendData()
            }, 500)
        }

        timerBox.innerHTML = `Осталось времени:   <b>${displayMinutes}:${displaySeconds}</b>`

    }, 1000)
}


var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

const sendData = () => {
    const data = {} // empty dictionary
    data['csrfmiddlewaretoken'] = csrfToken

    $.ajax({
        type: 'POST',
        url: `${url}submit/`,
        data: data,
        success: function (response) {
            const results = response.results
            console.log(results)
        },
        error: function (error) {
            console.log(error)
        }
    })
}
