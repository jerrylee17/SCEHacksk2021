import React, { Component } from 'react';
import counties from "../counties.json";
import Plot from "react-plotly.js";
import { get_scores } from '../helper/lambda';

class Map extends Component {
    constructor(props) {
        super(props);
        this.state = {data: this.runInference()};
    }

    async componentDidMount() {
        for (var i in counties['features']) {
            let feature = counties['features'][i];
            feature['id'] = feature['properties']['GEO_ID'].substring(9);
        }
        const data = await this.runInference()
        this.setState({
            data: data
        })
    }

    async runInference() {
        //make AWS lambda call here 
        // const inference = {
        //     'statusCode': 200, 
        //     'body': {'0': '1', '1': '0.01034', '2': '0.74', '3': '0.3752', '4': '0.02414',
        //                 '5': '0.5', '6': '0.6', '7': '0.7', '8': '0.8', '9': '0.9'}};
        const asyncResponse = await get_scores()
        const inference = JSON.parse(asyncResponse.Payload)
        const county_map = {'0': '06085', '1': '06087', '2': '06081', '3': '06075', '4': '06001', '5': '06077',
                            '6': '06099', '7': '06047', '8': '06069', '9': '06053'};
        const county_names = {
            '0': 'Santa Clara', 
            '1': 'Santa Cruz', 
            '2': 'San Mateo', 
            '3': 'San Francisco', 
            '4': 'Alameda',
            '5': 'San Joaquin', 
            '6': 'Stanislaus', 
            '7': 'Merced', 
            '8': 'San Benito', 
            '9': 'Monterey'
        };
        var idList = [];
        var valList = [];
        var nameList = [];
        for (var key in inference["body"]) {
            idList.push(county_map[key]);
            valList.push(inference["body"][key]);
            nameList.push(county_names[key]);
        }
        return {'id': idList, 'val': valList, 'name': nameList};
    }

    render() {
        console.log(this.state);
        return (
            <div>
                <Plot
                    data = {[{
                            type: "choropleth",
                            geojson: counties,
                            zmin: 0,
                            zmax: 1,
                            locations: this.state.data["id"],
                            z: this.state.data["val"],
                            text: this.state.data["name"]
                        }]}
                    layout = {{
                            width: 1500, height: 700,
                            geo: {fitbounds: "locations", visible: false},
                            margin: {r:0,t:0,l:0,b:0}
                        }}
                />
            </div>
        )
    }
}

export default Map;