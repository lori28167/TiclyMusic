# Changelog

## [Unreleased]
### Added
- Aggiunta la funzionalità di ricerca delle canzoni tramite Spotify.
- Implementata l'integrazione per il download di canzoni da YouTube tramite `yt-dlp`.
- Aggiunto il supporto per la riproduzione audio con VLC.
- Aggiunti i controlli di pausa, ripresa, e ripetizione per la gestione della riproduzione.
- Implementata la visualizzazione delle informazioni sulla canzone, come la durata e il tempo di riproduzione.

### Fixed
- Risolto un bug che impediva la corretta gestione del volume tramite il cursore.
- Corretto il processo di download della canzone che ora salva correttamente i file audio in formato `.webm`.
- Risolto un problema di interfaccia che non permetteva di interagire con i pulsanti in determinate condizioni.

### Changed
- Migliorato il flusso di interazione con l'utente, con messaggi di errore e successo.
- Ottimizzazione del processo di download dei brani tramite YouTube.

## [0.1.0] - 2024-12-18
### Initial Release
- Versione iniziale dell'app con supporto per la ricerca di brani musicali da Spotify.
- Supporto per il download e la riproduzione di brani da YouTube tramite `yt-dlp`.
- Implementazione base per il controllo della riproduzione musicale con VLC.
- Aggiunta l'interfaccia grafica con `tkinter` per la ricerca e la riproduzione della musica.
- Implementato il flusso di ricerca musicale tramite l'API di Spotify.
- Aggiunta la funzionalità di download e ascolto delle canzoni trovate, con VLC per la riproduzione.
- Implementate opzioni per mettere in pausa, riprendere e ripetere la riproduzione musicale.
- Aggiunta la gestione del volume tramite un cursore.
