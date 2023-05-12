const toggleColorTheme = () => {
    let darkMode = localStorage.getItem('darkMode');
    if (darkMode && eval(darkMode)) {
        $('#dark-mode').hide();
        $('#light-mode').show();
        $('.brand-image').attr('src', '/static/public/images/brand-image-white.png');
        $('.toggle-bg').addClass('bg-dark').removeClass('bg-light');
        $('.toggle-shadow').addClass('shadow-dark').removeClass('shadow-light');
        $('.toggle-border').addClass('border-dark').removeClass('border-light');
        $('.toggle-text').addClass('text-white').removeClass('text-dark');
        $('.toggle-text i').addClass('filter-to-white');
        $('#navbar').addClass('navbar-dark').removeClass('navbar-light');
        return true;
    } else {
        $('#dark-mode').show();
        $('#light-mode').hide();
        $('.brand-image').attr('src', '/static/public/images/brand-image.png');
        $('.toggle-bg').addClass('bg-light').removeClass('bg-dark');
        $('.toggle-shadow').addClass('shadow-light').removeClass('shadow-dark');
        $('.toggle-border').addClass('border-light').removeClass('border-dark');
        $('.toggle-text').addClass('text-dark').removeClass('text-white');
        $('.toggle-text i').removeClass('filter-to-white');
        $('#navbar').addClass('navbar-light').removeClass('navbar-dark');
        return false;
    }
}

const toggleDarkMode = (enable) => {
    if(enable) localStorage.setItem('darkMode', 'true');
    else localStorage.setItem('darkMode', 'false');
    location.reload();
}

const navigate = (url) => {
    location.assign(url);
}

const showSpinner = (message) => {
    if(message) {
        $('#spinner #spinner-message').addClass('pt-3')
        $('#spinner #spinner-message').html(message)
    } else {
        $('#spinner #spinner-message').removeClass('pt-3')
    }
    $('#spinner').show();
}

const hideSpinner = () => {
    $('#spinner').hide();
}

$(document).ready(() => {
    window.darkMode = toggleColorTheme();
    $("html").css("visibility", "visible");
});
