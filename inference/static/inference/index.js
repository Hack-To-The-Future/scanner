var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    created: function () {
        this.ws = new WebSocket(
            'ws://' + window.location.host + '/ws'
        );
        this.ws.onmessage = this.handle_message;
        this.ws.onclose = this.handle_close;
    },
    data: {
        ws: null,
        items: []
    },
    methods: {
        handle_message: function(e) {
            var data = JSON.parse(e.data);
            var prediction = data['prediction'];
            this.items = prediction;
            console.log(prediction);
        },
        handle_close: function(e) {
            console.error('Websocket Closed');
        }
    }
})



