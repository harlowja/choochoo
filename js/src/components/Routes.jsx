import React from 'react';
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import {Analysis, Diary, Welcome} from "./pages";
import {Change, Components, Snapshot} from "./pages/kit";


export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path='/' exact={true} component={Welcome}/>
                <Route path='/analysis' exact={true} component={Analysis}/>
                <Route path='/kit/change' exact={true} component={Change}/>
                <Route path='/kit/components' exact={true} component={Components}/>
                <Route path='/kit/:date' exact={true} component={Snapshot}/>
                <Route path='/:date' exact={true} component={Diary}/>
            </Switch>
        </BrowserRouter>
    );
}
