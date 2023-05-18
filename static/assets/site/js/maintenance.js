const init = () => {
    const newResultListHeight = $('#maintenance-view-container').height();
    if (newResultListHeight) {
        $('#deleted-files').height(newResultListHeight - 144);
    }

    $('#delete-config-form').hide();
    $('#maintenance-result').hide();
    $('#deleted-temp-files-container').hide();
    $('#deleted-recycle-bin-files-container').hide();
    $('#deleted-chrome-files-container').hide();
    $('#deleted-edge-files-container').hide();
    $('#deleted-opera-files-container').hide();
    $('#no-deleted-files-container').hide();

    showSpinner();
}

const checkBrowser = () => {
    const userAgent = navigator.userAgent;
    if (userAgent.match(/edg/i)) {
        if($('#edge-history').prop('checked') || $('#edge-cache').prop('checked') || $('#edge-cookies').prop('checked') || $('#edge-extensions').prop('checked') || $('#edge-passwords').prop('checked')) {
            return true;
        }
        return false;
    } else if (userAgent.match(/opr\//i)) {
        if($('#opera-history').prop('checked') || $('#opera-cache').prop('checked') || $('#opera-cookies').prop('checked') || $('#opera-extensions').prop('checked') || $('#opera-passwords').prop('checked')) {
            return true;
        }
        return false;
    // TODO: Uncomment when firefox method are implemented
    // } else if (userAgent.match(/firefox|fxios/i)) {
    //     if($('#firefox-history').prop('checked') || $('#firefox-cache').prop('checked') || $('#firefox-cookies').prop('checked') || $('#firefox-extensions').prop('checked') || $('#firefox-passwords').prop('checked')) {
    //         return true;
    //     }
    //     return false;
    } else if (userAgent.match(/chrome|chromium|crios/i)) {
        if($('#chrome-history').prop('checked') || $('#chrome-cache').prop('checked') || $('#chrome-cookies').prop('checked') || $('#chrome-extensions').prop('checked') || $('#chrome-passwords').prop('checked')) {
            return true;
        }
        return false;
    } else {
        return false;
    }
}

const showResult = (data) => {
    let tempContent = '';
    let recycleContent = '';
    let chromeContent = '';
    let edgeContent = '';
    let operaContent = '';
    if (data.temp_files && data.temp_files.deletedFiles.length) {
        for (const path of data.temp_files.deletedFiles) {
            tempContent = tempContent + `<div class="ps-3">${path}</div>`;
        }
        $('#deleted-temp-files').html(tempContent);
        $('#deleted-temp-files-container').show();
    }
    if (data.recycle_bin && data.recycle_bin.deletedFiles.length) {
        for (const path of data.recycle_bin.deletedFiles) {
            recycleContent = recycleContent + `<div class="ps-3">${path}</div>`;
        }
        $('#deleted-recycle-bin-files').html(recycleContent);
        $('#deleted-recycle-bin-files-container').show();
    }
    if (data.browsers && data.browsers.deletedFiles.length) {
        for (const path of data.browsers.deletedFiles) {
            if (path.toLowerCase().includes('chrome')) {
                chromeContent = chromeContent + `<div class="ps-3">${path}</div>`;
            } else if (path.toLowerCase().includes('edge')) {
                edgeContent = edgeContent + `<div class="ps-3">${path}</div>`;
            } else if (path.toLowerCase().includes('opera')) {
                operaContent = operaContent + `<div class="ps-3">${path}</div>`;
            }
        }
        if (chromeContent) {
            $('#deleted-chrome-files').html(chromeContent);
            $('#deleted-chrome-files-container').show();
        }
        if (edgeContent) {
            $('#deleted-edge-files').html(edgeContent);
            $('#deleted-edge-files-container').show();
        }
        if (operaContent) {
            $('#deleted-opera-files').html(operaContent);
            $('#deleted-opera-files-container').show();
        }
    }
    if (!tempContent && !recycleContent && !chromeContent && !edgeContent && !operaContent) {
        $('#no-deleted-files-container').show();
    }
    $('#maintenance-result #deleted').html(data.deleted);
    $('#maintenance-result #skipped').html(data.skipped);
    hideSpinner();
    $('#maintenance-result').show();
}

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
        showResult(response.data)
    } catch (error) {
        $('#maintenance-result').html(`${error.status}: ${error.responseText}`);
    }
}

const submitData = async () => {
    confirmModal = new bootstrap.Modal(document.getElementById('confirm-modal'));
    if (checkBrowser()) {
        confirmModal.show();
    } else {
        await sendData();
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

init();

$(document).ready(async () => {
    await getData();
    hideSpinner();
    $('#delete-config-form').show();
});
