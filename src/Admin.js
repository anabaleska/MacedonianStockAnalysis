import React from 'react';
import HistoricDataInput from "./components/admin/HistoricDataInput";
import TableHeader from "./components/admin/TableHeader";


const Admin = () => {
    return (
        <div>
            <HistoricDataInput/>
            <TableHeader/>
        </div>
    );
};

export default Admin;