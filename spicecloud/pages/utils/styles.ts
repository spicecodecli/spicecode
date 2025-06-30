export const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f0e3c8, #e3d6b0, #d7b377)',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: '#000000'
  },
  header: {
    background: 'rgba(215, 179, 119, 0.9)',
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid rgba(160, 130, 60, 0.8)',
    position: 'sticky' as const,
    top: 0,
    zIndex: 40,
    padding: '1rem 1.5rem',
    color: '#000000',
  },
  headerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    maxWidth: '1200px',
    margin: '0 auto'
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#000000',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem'
  },
  subtitle: {
    color: 'rgba(0, 0, 0, 0.7)',
    marginTop: '0.25rem'
  },
  refreshButton: {
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    fontWeight: '500',
    transition: 'all 0.2s',
    border: 'none',
    cursor: 'pointer',
    color: '#000000',
  },
  mainContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem 1.5rem',
    display: 'grid',
    gridTemplateColumns: 'minmax(300px, 1fr) 2fr',
    gap: '2rem'
  },
  sidebar: {
    background: 'rgba(215, 179, 119, 0.25)',
    backdropFilter: 'blur(10px)',
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    height: 'fit-content',
    position: 'sticky' as const,
    top: '6rem',
    color: '#000000'
  },
  sidebarTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#000000',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  fileList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem',
    maxHeight: '60vh',
    overflowY: 'auto' as const
  },
  fileItem: {
    padding: '1rem',
    borderRadius: '0.75rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    border: '1px solid rgba(160, 130, 60, 0.3)',
    background: 'rgba(215, 179, 119, 0.1)',
    color: '#000000',
  },
  fileItemSelected: {
    background: 'linear-gradient(45deg, #d97304, #a35402)',
    color: '#000000',
    transform: 'scale(1.02)',
    boxShadow: '0 10px 25px rgba(217, 115, 4, 0.5)'
  },
  fileItemDefault: {
    background: 'rgba(215, 179, 119, 0.1)',
    color: '#000000'
  },
  fileInfo: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '0.75rem'
  },
  fileIcon: {
    fontSize: '1.25rem'
  },
  fileName: {
    fontWeight: '500',
    fontSize: '0.875rem',
    marginBottom: '0.25rem'
  },
  filePath: {
    fontSize: '0.75rem',
    opacity: 0.7,
    marginBottom: '0.5rem'
  },
  fileAge: {
    fontSize: '0.75rem',
    opacity: 0.7,
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem'
  },
  metricsArea: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1.5rem'
  },
  fileHeader: {
    background: 'linear-gradient(135deg, rgba(215, 179, 119, 0.3), rgba(160, 130, 60, 0.2))',
    backdropFilter: 'blur(10px)',
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    color: '#000000'
  },
  fileHeaderContent: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '1rem'
  },
  fileHeaderIcon: {
    fontSize: '2.5rem'
  },
  fileHeaderTitle: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#000000',
    marginBottom: '0.5rem'
  },
  fileHeaderPath: {
    color: 'rgba(0, 0, 0, 0.7)',
    fontSize: '0.875rem',
    marginBottom: '0.5rem'
  },
  fileHeaderMeta: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
    fontSize: '0.875rem',
    color: 'rgba(0, 0, 0, 0.5)'
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '1.5rem'
  },
  metricCard: {
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    backdropFilter: 'blur(10px)',
    background: 'rgba(217, 115, 4, 0.15)',
    transition: 'all 0.2s',
    cursor: 'default',
    color: '#000000'
  },
  metricHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '1rem',
    color: '#000000'
  },
  metricIcon: {
    fontSize: '1.5rem',
    transition: 'transform 0.2s'
  },
  metricTitle: {
    fontWeight: '600',
    color: '#000000',
    fontSize: '1.125rem'
  },
  metricValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#000000',
    marginBottom: '0.5rem'
  },
  progressBar: {
    width: '100%',
    height: '0.5rem',
    background: 'rgba(160, 130, 60, 0.3)',
    borderRadius: '0.25rem',
    marginTop: '0.75rem',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    background: 'linear-gradient(90deg, #d97304, #a35402)',
    borderRadius: '0.25rem',
    transition: 'width 1s ease'
  },
  methodTypeCard: {
    background: 'linear-gradient(135deg, rgba(217, 115, 4, 0.2), rgba(161, 84, 2, 0.2))',
    border: '1px solid rgba(217, 115, 4, 0.2)',
    color: '#000000'
  },
  methodTypeList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem'
  },
  methodTypeItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0.75rem',
    background: 'rgba(160, 130, 60, 0.1)',
    borderRadius: '0.5rem',
    color: '#000000'
  },
  methodTypeLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  methodTypeDot: {
    width: '0.75rem',
    height: '0.75rem',
    borderRadius: '50%'
  },
  methodTypeText: {
    color: '#000000'
  },
  methodTypeValue: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    color: '#000000'
  },
  indentationCard: {
    background: 'linear-gradient(135deg, rgba(217, 115, 4, 0.2), rgba(161, 84, 2, 0.2))',
    border: '1px solid rgba(217, 115, 4, 0.2)',
    color: '#000000'
  },
  indentationList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem'
  },
  indentationItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: '#000000'
  },
  indentationLabel: {
    color: '#000000'
  },
  indentationValue: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#000000'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f0e3c8, #e3d6b0, #d7b377)',
    color: '#000000'
  },
  loadingSpinner: {
    width: '4rem',
    height: '4rem',
    border: '4px solid rgba(217, 115, 4, 0.3)',
    borderTop: '4px solid #d97304',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  },
  emptyState: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '24rem',
    color: '#000000'
  },
  emptyStateContent: {
    textAlign: 'center' as const
  },
  emptyStateIcon: {
    fontSize: '3.75rem',
    marginBottom: '1rem',
    opacity: 0.5
  },
  emptyStateText: {
    color: 'rgba(0, 0, 0, 0.7)',
    fontSize: '1.25rem'
  },
  fileIconImg: { width: '1.5rem', height: '1.5rem', objectFit: 'contain' as const },
  fileHeaderImg: { width: '3rem', height: '3rem', objectFit: 'contain' as const }
};