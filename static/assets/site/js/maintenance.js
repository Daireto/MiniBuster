const sendData = async () => {
    try {
        $('#delete-config-form').hide();
        showSpinner('Realizando limpieza. Esto puede tomar unos minutos.');

        config = {
            system: {
                temp_files: $('#system-temp_files').prop('checked'),
                recycle_bin: $('#system-recycle_bin').prop('checked'),
            },
            browsers: {
                chrome: {
                    history: $('#chrome-history').prop('checked'),
                    cache: $('#chrome-cache').prop('checked'),
                    cookies: $('#chrome-cookies').prop('checked'),
                    extensions: $('#chrome-extensions').prop('checked'),
                    passwords: $('#chrome-passwords').prop('checked'),
                },
                edge: {
                    history: $('#edge-history').prop('checked'),
                    cache: $('#edge-cache').prop('checked'),
                    cookies: $('#edge-cookies').prop('checked'),
                    extensions: $('#edge-extensions').prop('checked'),
                    passwords: $('#edge-passwords').prop('checked'),
                },
                opera: {
                    history: $('#opera-history').prop('checked'),
                    cache: $('#opera-cache').prop('checked'),
                    cookies: $('#opera-cookies').prop('checked'),
                    extensions: $('#opera-extensions').prop('checked'),
                    passwords: $('#opera-passwords').prop('checked'),
                }
            }
        }

        const response = await post('/maintenance', config);
        $('#maintenance-result #deleted').html(response.data.deleted);
        hideSpinner();
        $('#maintenance-result').show();
    } catch (error) {
        $('#maintenance-result').html(`${error.status}: ${error.responseText}`);
    }
}

const getData = async () => {
    const config = await get('/maintenance/get_config');
    $('#system-temp_files').prop('checked', config.system.temp_files);
    $('#system-recycle_bin').prop('checked', config.system.recycle_bin);
    $('#chrome-history').prop('checked', config.browsers.chrome.history);
    $('#chrome-cache').prop('checked', config.browsers.chrome.cache);
    $('#chrome-cookies').prop('checked', config.browsers.chrome.cookies);
    $('#chrome-extensions').prop('checked', config.browsers.chrome.extensions);
    $('#chrome-passwords').prop('checked', config.browsers.chrome.passwords);
    $('#edge-history').prop('checked', config.browsers.edge.history);
    $('#edge-cache').prop('checked', config.browsers.edge.cache);
    $('#edge-cookies').prop('checked', config.browsers.edge.cookies);
    $('#edge-extensions').prop('checked', config.browsers.edge.extensions);
    $('#edge-passwords').prop('checked', config.browsers.edge.passwords);
    $('#opera-history').prop('checked', config.browsers.opera.history);
    $('#opera-cache').prop('checked', config.browsers.opera.cache);
    $('#opera-cookies').prop('checked', config.browsers.opera.cookies);
    $('#opera-extensions').prop('checked', config.browsers.opera.extensions);
    $('#opera-passwords').prop('checked', config.browsers.opera.passwords);
}

$(document).ready(async () => {
    await getData();
    hideSpinner();
    $('#delete-config-form').show();
});

$('#delete-config-form').hide();
$('#maintenance-result').hide();
showSpinner();
