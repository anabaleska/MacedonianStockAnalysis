import React, {useEffect, useState} from "react";
import styles from './TableHeader.module.css';
import TransactionItem from "./TransactionItem";

const TableHeader = () => {

    const [details, setDetails] = useState([]);
    const [currentPage, setCurrentPage] = useState(0); // State for current page
    const [totalPages, setTotalPages] = useState(0);

    const fetchPage = (currentPage) => {
        fetch(`http://localhost:8081/api/ticker-values?page=${currentPage}&size=20`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Details fetched:", data);
                setDetails(data.content || []); // Extract content property
                setTotalPages(data.totalPages || 0); // Set total pages from API
            })
            .catch((error) => console.error("Error fetching details:", error));
    };

    useEffect(() => {
        fetchPage(currentPage)
    }, [currentPage]);

    const handleNext = () => {
        if (currentPage < totalPages - 1) {
            setCurrentPage((prevPage) => prevPage + 1);
        }
    };

    const handlePrevious = () => {
        if (currentPage > 0) {
            setCurrentPage((prevPage) => prevPage - 1);
        }
    };


    const headers = [
        {id: 'ticker', label: 'Ticker'},
        {id: 'max', label: 'Max'},
        {id: 'min', label: 'Min'},
        {id: 'date', label: 'Date'},
        {id: 'lastPrice', label: 'Price of last\ntransaction', isLast: true}
    ];

    const handleDelete = (code) => {
        console.log("Delete transaction with code:", code);
        // Handle delete logic here (e.g., API call to delete, and update state)
    };

    const handleEdit = (code) => {
        console.log("Edit transaction with code:", code);
        // Handle edit logic here
    };

    return (
        <div className={styles.tableWrapper}>
            {/* Table Header */}
            <div className={styles.tableHeader}>
                <div className={styles.headerRow} role="row">
                    {headers.map((header) => (
                        <div
                            key={header.id}
                            className={header.isLast ? styles.lastPriceCell : styles.headerCell}
                            role="columnheader"
                            tabIndex={0}
                        >
                            {header.label}
                        </div>
                    ))}
                </div>
            </div>

            {/* Table Body */}
            <div className={styles.tableBody}>
                {details.length === 0 ? (
                    <div>No data available</div>
                ) : (
                    details.map((row) => (
                        <TransactionItem
                        key={row.value_id}
                        transactionData={row}
                        onDelete={handleDelete}
                        onEdit={handleEdit}
                        />
                    ))
                )}
            </div>
            {/* Pagination Controls */}
            <div className={styles.paginationControls}>
                <button onClick={handlePrevious} disabled={currentPage === 0}>
                    Previous
                </button>
                <span>
                    Page {currentPage + 1} of {totalPages}
                </span>
                <button
                    onClick={handleNext}
                    disabled={currentPage >= totalPages - 1}
                >
                    Next
                </button>
            </div>

        </div>
    )
};

export default TableHeader;