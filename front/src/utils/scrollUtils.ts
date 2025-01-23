export const scrollToElement = (element: HTMLElement | null) => {
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'end'
    });
  }
};