-- File di test per le query sql

SELECT Giorno, OraInizio, Durata, COUNT(*)
FROM programma
GROUP BY Giorno, OraInizio, Durata;