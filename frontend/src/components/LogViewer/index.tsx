import type { API } from '@/utils/API';

import { Card } from '..';

import { useState, useEffect } from 'react';

interface LogViewerProps {
    api: API
}
export function LogViewer({ api }: LogViewerProps) {
    const [logs, setLogs] = useState<string[]>([]);
    const [page, setPage] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    function handleScroll() {
        if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight || isLoading) {
            return;
        }
        setPage(page+1)
    };
-
    useEffect(() => {
        setIsLoading(true);
        api.getLog(page).then(res => {
            setLogs([...res, ...logs]);
            setIsLoading(false);
        });
    }, [page]);

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [isLoading]);

    return (
        <Card>
            <ul>
                {logs.map((l, i) =>
                    <li key={i}>{l}</li>
                )}
            </ul>
        </Card>
    )
}