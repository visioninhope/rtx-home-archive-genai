$(document).ready(function() {

$('#searchBtn').click(function() {
    var prompt = $('#prompt').val();
    var selectedTags = $('.tag.bg-indigo-600').map(function() {
        return $(this).data('id');
    }).get();

    $.get('/browse', { prompt: prompt, 'tags[]': selectedTags }, function(data) {
        if (Array.isArray(data)) {
            var content = data.map(function(doc) {
                // Process the complex tags structure
                var tags = doc.tags.tags;
                console.log(tags);
                
                // Only display the tags paragraph if there are tags after processing
                var tagsDisplay = tags.length > 0 ? `<p>Tags: ${tags}</p>` : '';

                // Assuming doc.url is something like "/documents/abc.pdf"
                var docName = doc.url.split('/').pop().split('.').slice(0, -1).join('.'); // Extracts "abc" from "abc.pdf"
                var textContentUrl = `/explore_document?docName=${docName}.txt`; // Construct URL for the text content

                // Modify the fancyCard string to include the new link
                var fancyCard = `<div class="bg-white rounded-lg border border-gray-200 shadow-md p-6 mx-4 text-center card-bg mb-4">
                                    ...
                                    <a href="${doc.url}" target="_blank" class="text-indigo-600 hover:text-indigo-800">
                                        <i class="fas fa-file-alt"></i> View Document
                                    </a>
                                    <a href="${textContentUrl}" target="_blank" class="text-green-600 hover:text-green-800 ml-4">
                                        <i class="fas fa-ai"></i> Explore Document with AI
                                    </a>
                                    ${tagsDisplay}
                                    </p>
                                    <p class="text-justify">${doc.text}</p>
                                </div>`;

                return fancyCard;
            }).join('');
            
            $('#searchResults').html(content);

            // Attach event listener to "View Document" links
            $('.view-document').click(function(e) {
                e.preventDefault();
                var url = $(this).attr('href');

                // Call the explain_text endpoint to get the explanation for the selected text
                $.post('/explain_text', { selectedText: $(this).siblings('p').text() }, function(response) {
                    // Open a new tab with the document content and the explanation
                    var newTab = window.open('', '_blank');
                    newTab.document.write(`
                        <!DOCTYPE html>
                        <html lang="en" class="flex flex-col min-h-screen">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Document View</title>
                            <!-- Add your stylesheets and scripts here -->
                        </head>
                        <body class="text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900 flex flex-col flex-1 transition-colors duration-500">
                            <div class="container mx-auto px-4 py-8">
                                <div class="mx-auto max-w-4xl my-8 bg-gray-200 dark:bg-gray-700 rounded-lg shadow overflow-hidden">
                                    ${url.includes('.txt') ? '<pre>' : ''}${response.text}${url.includes('.txt') ? '</pre>' : ''}
                                </div>
                            </div>
                        </body>
                        </html>
                    `);
                });
            });
        } else {
            $('#searchResults').html('<p class="text-red-500">No results found or an error occurred.</p>');
        }
    }).fail(function() {
        $('#searchResults').html('<p class="text-red-500">No results found or an error occurred.</p>');
    });
});



    
});
