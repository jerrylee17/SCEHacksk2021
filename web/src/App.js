import React from "react";
import Map from "./Map";

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
        <div class="container">
          <h1>Arson</h1>
          <Map/>
          <form onSubmit={this.handleSubmit}>
            <textarea type="text" onChange={this.handleChange}>{this.state.text}</textarea>
            <br />
            <input class="btn btn-primary" type="submit" value="Submit" />
          </form>
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
