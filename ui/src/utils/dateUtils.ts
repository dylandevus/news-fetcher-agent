/**
 * Format a date string into a friendly relative time format (e.g., "2d")
 * @param dateString - The date string to format
 * @returns Formatted date string like "2d", "3h", etc.
 */
export const formatRelativeDate = (dateString?: string): string => {
  if (!dateString) return "";
  
  const date = new Date(dateString);
  const now = new Date();
  
  // Return empty string for invalid dates
  if (isNaN(date.getTime())) return "";
  
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  const diffMonth = Math.floor(diffDay / 30);
  const diffYear = Math.floor(diffMonth / 12);
  
  if (diffYear > 0) return `${diffYear}y`;
  if (diffMonth > 0) return `${diffMonth}mo`;
  if (diffDay > 0) return `${diffDay}d`;
  if (diffHour > 0) return `${diffHour}h`;
  if (diffMin > 0) return `${diffMin}m`;
  return "just now";
};
