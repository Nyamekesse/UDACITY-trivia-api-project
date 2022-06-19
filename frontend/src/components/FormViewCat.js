import React, { Component } from "react";
import $ from "jquery";
import "../stylesheets/FormView.css";

class FormView extends Component {
  constructor(props) {
    super();
    this.state = {
      category: "",
    };
  }

  componentDidMount() {
    $.ajax({
      url: `/api/categories`,
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories });
        return;
      },
      error: (error) => {
        alert("Unable to load categories. Please try your request again");
        return;
      },
    });
  }

  submitCategory = (event) => {
    event.preventDefault();
    $.ajax({
      url: "/api/categories/new-category",
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-category-form").reset();
        return;
      },
      error: (error) => {
        alert("Unable to add category. Please try your request again");
        return;
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id="add-form">
        <h2>Add New Category</h2>
        <form
          className="form-view"
          id="add-category-form"
          onSubmit={this.submitCategory}
        >
          <label>
            Type
            <input type="text" name="category" onChange={this.handleChange} />
          </label>

          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;
