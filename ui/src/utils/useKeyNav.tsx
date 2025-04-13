import { useEffect, useState, RefObject } from 'react';

interface UseKeyNavOptions<T> {
  items: T[];
  containerRef: RefObject<HTMLElement>;
onSelect?: (item: T, isOpeningLink?: boolean) => void;
  getItemId?: (item: T) => string;
  customActions?: {
    [key: string]: (currentItem: T, index: number) => void;
  };
  autoSelectOnKeyPress?: boolean;
  deps?: any[];
}

interface UseKeyNavResult<T> {
  activeIndex: number;
  setActiveIndex: (index: number) => void;
  activeItemId: string | null;
  handleItemClick: (item: T, index: number) => void;
}

function useKeyNav<T>({
  items,
  containerRef,
  onSelect,
  getItemId = (item: any) => item.id,
  customActions = {},
  deps = []
}: UseKeyNavOptions<T>): UseKeyNavResult<T> {
  const [activeIndex, setActiveIndex] = useState<number>(-1);
  const [activeItemId, setActiveItemId] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!items || items.length === 0) return;

      let currentIndex = activeIndex;

      switch (e.key) {
        case 'ArrowUp':
          e.preventDefault();
          currentIndex = Math.max(0, currentIndex - 1);
          setActiveIndex(currentIndex);
          setActiveItemId(getItemId(items[currentIndex]) || null);
          // Call onSelect when navigating up
          if (onSelect && currentIndex >= 0) {
            onSelect(items[currentIndex]);
          }
          break;
        case 'ArrowDown':
          e.preventDefault();
          currentIndex = Math.min(items.length - 1, currentIndex + 1);
          setActiveIndex(currentIndex);
          setActiveItemId(getItemId(items[currentIndex]) || null);
          // Call onSelect when navigating down
          if (onSelect && currentIndex >= 0) {
            onSelect(items[currentIndex]);
          }
          break;
        case 'Enter':
          // Only handle Meta (Cmd) + Enter, not regular Enter
          if (e.metaKey && currentIndex >= 0 && currentIndex < items.length) {
            const item = items[currentIndex];
            if (onSelect) {
              onSelect(item, true); // Pass true to indicate metaKey is pressed
            }
          }
          break;
        default:
          // Handle custom key actions
          if (customActions[e.key] && currentIndex >= 0) {
            customActions[e.key](items[currentIndex], currentIndex);
          }
          break;
      }

      // Scroll the active item into view if needed
      if (currentIndex >= 0) {
        const activeElement = containerRef.current?.querySelector(`[data-index="${currentIndex}"]`);
        activeElement?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [items, activeIndex, onSelect, getItemId, containerRef, customActions, ...deps]);

  const handleItemClick = (item: T, index: number) => {
    setActiveIndex(index);
    setActiveItemId(getItemId(item) || null);
    if (onSelect) {
      onSelect(item);
    }
  };

  return {
    activeIndex,
    setActiveIndex,
    activeItemId,
    handleItemClick
  };
}

export default useKeyNav;
