const sendData = async () => {
    const data = {
        message: 'Hello, World!'
    };
    const response = await post('maintenance', data);
    alert(response.message)
}
