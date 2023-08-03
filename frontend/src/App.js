import React, { Component } from "react";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewCompleted: false,
      todoList: [],
      modal: false,
      activeItem: {
        title: "",
        description: "",
        completed: false,
      },
    };
  }

  componentDidMount() {
    this.refreshList();
  }

  refreshList = () => {
    axios
      .get("/api/todos/")
      .then((res) => this.setState({ todoList: res.data }))
      .catch((err) => console.log(err));
  };


  render() {
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">bus app</h1>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            
          </div>
        </div>
      </main>
    );
  }
}

export default App;
