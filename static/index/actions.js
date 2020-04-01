class Actions {
    constructor(sender) {
        this.sender = sender;
    }

    send_action(action_name) {
        let json = {
            "name": action_name,
            "options": controllers.get_options()
        };
        this.sender.post('/quickaction', json, this.success_action);
    }

    success_action(recieved) {
        console.log("Sucessfully recieved action", recieved);
    }

}