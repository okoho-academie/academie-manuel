// Académie-Orbit : une orbite, cinq jalons, le jalon en cours en orange.
export function Orbit({ className = '' }: { className?: string }) {
  return (
    <svg viewBox="0 0 400 300" className={className} aria-hidden="true" preserveAspectRatio="xMidYMid meet">
      <ellipse cx="230" cy="150" rx="190" ry="62" transform="rotate(-20 230 150)" fill="none" stroke="#6B9CD1" strokeWidth="1.5" opacity=".6"/><circle cx="66" cy="214" r="6" fill="#6B9CD1"/><circle cx="148" cy="187" r="6" fill="#6B9CD1"/><circle cx="232" cy="152" r="8" fill="#FFA142"/><circle cx="318" cy="112" r="6" fill="none" stroke="#6B9CD1" strokeWidth="2"/><circle cx="398" cy="77" r="6" fill="none" stroke="#6B9CD1" strokeWidth="2"/>
    </svg>
  );
}
