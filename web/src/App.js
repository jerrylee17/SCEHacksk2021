import React from "react";
import Map from "./components/Map";

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
      text: "", 
      counties: [] 
    }
    this.handleSubmit = this.handleSubmit.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  // OnTextSubmit runs code upon submitting the text
  handleSubmit(event) {
    event.preventDefault()
    // TODO: some logic
    console.log(this.state.text)
  }
//asd
  // handleTextChange updates the state's text upon typing into the textarea
  handleChange(event) {
    this.setState({ text: event.target.value })
    console.log(this.state.counties)
  }

  render() {
    return (
      <div class="App">
        <nav class="navbar navbar-dark bg-dark text-center">
          <div class="container-fluid justify-content-center navbar-brand">Arson Map</div>
        </nav>
        <div class="container">
          <Map/>
          {/* <form onSubmit={this.handleSubmit}>
            <textarea type="text" onChange={this.handleChange}>{this.state.text}</textarea>
            <br />
            <input class="btn btn-primary" type="submit" value="Submit" />
          </form> */}
          <div>
            
          </div>
          
        </div>
      </div>
    )
  }

  async componentDidMount() {
    // 
  }
}

export default App;
