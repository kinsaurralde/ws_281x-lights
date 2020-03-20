class Actions {
    constructor(sender, options=null) {
        this.sender = sender;
        this.options = options
    }

    send_action(action_name) {
        let json = {
            "name": action_name,
            "options": this.options
        };
        this.sender.post('/quickaction', json, this.success_action);
    }

    success_action(recieved) {
        console.log("Sucessfully recieved action", recieved);
    }

}