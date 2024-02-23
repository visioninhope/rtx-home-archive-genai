$(document).ready(function() {


    // Speech Recognition setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.onstart = function () {
        console.log('Voice is activated');
        // Change button color to red while recording
        $('#voice').css('background-color', 'red');
    };

    recognition.onend = function () {
        console.log('Voice is deactivated');
        // Change button color back to original (or any color you want) when done
        $('#voice').css('background-color', 'green');
    };

    recognition.onresult = function (event) {
        const transcript = event.results[0][0].transcript;
        $('#prompt').val(transcript);
    };

    // Voice button event listener
    $('#voice').on('click', function() {
        recognition.start();
    });

 // Load tags dynamically from the static folder
 $.getJSON('/static/data/tags.json', function(tags) {
    $.each(tags, function(i, tag) {
        $('#tagSelection').append(
            `<div class="tag flex items-center px-3 py-1 border rounded cursor-pointer select-none transition-colors ease-in-out duration-150" data-id="${tag.id}" style="margin-right: 5px; margin-bottom: 5px;">
                <i class="${tag.icon} mr-2"></i>
                <span>${tag.name}</span>
            </div>`
        );
    });
    
    // Handle tag selection
    $(document).on('click', '.tag', function() {
        $(this).toggleClass('bg-indigo-600 text-white'); // Visually toggle selection
    });
});
$('#uploadBtn').click(function(e) {
    e.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById('file');
    var docDesc = $('#prompt').val(); // Make sure to get the value
    if(fileInput.files.length === 0) {
        alert('Please select a file.');
        return;
    }
    var fileName = fileInput.files[0].name;
    formData.append('file', fileInput.files[0]);
    formData.append('docDesc', docDesc);
    
    $('.tag.bg-indigo-600').each(function() {
        formData.append('tags[]', $(this).data('id'));
    });

    // Show the popup
    $('#uploadPopup').removeClass('hidden');

    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            $('#uploadResult').html(`<p class="text-green-500">${fileName}: ${data.message}</p>`);
            // Hide the popup
            $('#uploadPopup').addClass('hidden');
        },
        error: function(xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText;
            $('#uploadResult').html(`<p class="text-red-500">Error processing ${fileName} - ${errorMessage}</p>`);
            // Hide the popup even if there's an error
            $('#uploadPopup').addClass('hidden');
        }
    }); 
});

    
    
});
